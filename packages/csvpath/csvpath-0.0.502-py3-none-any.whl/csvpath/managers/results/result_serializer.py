import os
import json
import csv
from typing import NewType, List, Dict, Optional, Union
from datetime import datetime
from csvpath import CsvPath
from csvpath.matching.util.runtime_data_collector import RuntimeDataCollector
from csvpath.util.line_spooler import LineSpooler

Simpledata = NewType("Simpledata", Union[None | str | int | float | bool])
Listdata = NewType("Listdata", list[None | str | int | float | bool])
Csvdata = NewType("Csvdata", list[List[str]])
Metadata = NewType("Metadata", Dict[str, Simpledata])


class ResultSerializer:
    def __init__(self, base_dir: str):
        # archive dir from config.ini
        self.base_dir = base_dir
        self.result = None

    def save_result(self, result) -> None:
        self.result = result
        runtime_data = {}
        RuntimeDataCollector.collect(result.csvpath, runtime_data, local=True)
        runtime_data["run_index"] = result.run_index
        es = []
        if result is not None and result.errors:
            es = [e.to_json() for e in result.errors]
        self._save(
            metadata=result.csvpath.metadata,
            errors=es,
            variables=result.variables,
            lines=result.lines,
            printouts=result.printouts,
            runtime_data=runtime_data,
            paths_name=result.paths_name,
            file_name=result.file_name,
            identity=result.identity_or_index,
            run_time=result.run_time,
            run_dir=result.run_dir,
            run_index=result.run_index,
            unmatched=result.unmatched,
        )
        self.result = None

    def _save(
        self,
        *,
        metadata: Metadata,
        runtime_data: Metadata,
        errors: List[Metadata],
        variables: dict[str, Simpledata | Listdata | Metadata],
        lines: Csvdata,
        printouts: dict[str, list[str]],
        paths_name: str,
        file_name: str,
        identity: str,
        run_time: datetime,
        run_dir: str,
        run_index: int,
        unmatched: list[Listdata],
    ) -> None:
        """Save a single Result object to basedir/paths_name/run_time/identity_or_index."""
        meta = {
            "paths_name": paths_name,
            "file_name": file_name,
            "run_time": f"{run_time}",
            "run_index": run_index,
            "identity": identity,
            "metadata": metadata,
            "runtime_data": runtime_data,
        }
        run_dir = self.get_instance_dir(run_dir=run_dir, identity=identity)
        # Save the JSON files
        with open(os.path.join(run_dir, "meta.json"), "w") as f:
            json.dump(meta, f, indent=2)
        with open(os.path.join(run_dir, "errors.json"), "w") as f:
            json.dump(errors, f, indent=2)
        with open(os.path.join(run_dir, "vars.json"), "w") as f:
            json.dump(variables, f, indent=2)
        # Save lines returned as a CSV file. note that they may have already
        # spooled and the spooler been discarded.
        if lines is not None:
            if isinstance(lines, LineSpooler) and lines.closed is True:
                self.result.csvpath.logger.debug(
                    "line spooler has already written its data"
                )
            elif isinstance(lines, LineSpooler):
                self.result.csvpath.logger.debug(
                    "not writing data in/from line spooler even though lines.closed is not True"
                )
            else:
                #
                # this may not be right, but I think we can/maybe should not write data unless
                # we have some. that would match the possible spooler behavior. it would also
                # match fast_forward, which might be confusing, but if we capture the what method
                # a run used that's not a worry. and if we don't, not having a data file is a
                # poor indicator of the method anyway.
                #
                if lines is not None and len(lines) > 0:
                    with open(os.path.join(run_dir, "data.csv"), "w") as f:
                        writer = csv.writer(f)
                        writer.writerows(lines)
        #
        # writing is not needed. LineSpoolers are intended to stream their
        # lines to disk. if we write here we'll be reading and writing the
        # same file at the same time.
        #
        if (
            unmatched is not None
            and not isinstance(unmatched, LineSpooler)
            and len(unmatched) > 0
        ):
            with open(os.path.join(run_dir, "unmatched.csv"), "w") as f:
                writer = csv.writer(f)
                writer.writerows(unmatched)

        # Save the printout lines
        if self._has_printouts(printouts):
            with open(os.path.join(run_dir, "printouts.txt"), "w") as f:
                for k, v in printouts.items():
                    f.write(f"---- PRINTOUT: {k}\n")
                    for _ in v:
                        f.write(f"{_}\n")

    def _has_printouts(self, pos) -> bool:
        if pos is None:
            return False
        if len(pos) == 0:
            return False
        for k, v in pos.items():
            if v is not None and len(v) > 0:
                return True
        return False

    def _deref_paths_name(self, paths_name) -> str:
        #
        # if we have a reference we need to de-ref so that our path has only
        # the named-paths name at the top, not the $, datatype, etc.
        #
        paths_name = paths_name.lstrip("$")
        i = paths_name.find(".")
        if i > -1:
            paths_name = paths_name[0:i]
        i = paths_name.find("#")
        if i > -1:
            paths_name = paths_name[0:i]
        return paths_name

    def get_run_dir_name_from_datetime(self, dt) -> str:
        if dt is None:
            return None
        t = dt.strftime("%Y-%m-%d_%I-%M-%S")
        return t

    def get_run_dir(self, *, paths_name, run_time):
        paths_name = self._deref_paths_name(paths_name)
        run_dir = os.path.join(self.base_dir, paths_name)
        if not os.path.exists(run_dir):
            os.makedirs(run_dir, exist_ok=True)
        if not isinstance(run_time, str):
            run_time = self.get_run_dir_name_from_datetime(
                run_time
            )  # run_time.strftime("%Y-%m-%d_%I-%M-%S")
        run_dir = os.path.join(run_dir, f"{run_time}")
        # the path existing for a different named-paths run in progress
        # or having completed less than 1000ms ago is expected to be
        # uncommon in real world usage. CsvPaths are single user instances
        # atm. a server process would namespace each CsvPaths instance
        # to prevent conflicts. if there is a conflict the two runs would
        # overwrite each other. this prevents that.
        if os.path.exists(run_dir):
            i = 0
            adir = f"{run_dir}.{i}"
            while os.path.exists(adir):
                i += 1
                adir = f"{run_dir}.{i}"
            run_dir = adir
        return run_dir

    def get_instance_dir(self, run_dir, identity) -> str:
        run_dir = os.path.join(run_dir, identity)
        os.makedirs(run_dir, exist_ok=True)
        return run_dir

    """
    def load_result(self, paths_name: str, run_time: str, identity: str):
        ""Load a single Result object from the base directory.""
        run_dir = self._run_dir(
            paths_name=paths_name, run_time=run_time, identity=identity
        )
        if not os.path.exists(run_dir):
            return None
        return self._load_result(run_dir)

    def _load_result(self, run_dir: str):
        if not os.path.exists(run_dir):
            return None
        try:
            meta = None
            variables = None
            errors = None
            data = None
            printouts = None

            with open(os.path.join(run_dir, "meta.json"), "r") as f:
                meta = json.load(f)
            with open(os.path.join(run_dir, "vars.json"), "r") as f:
                variables = json.load(f)
            with open(os.path.join(run_dir, "errors.json"), "r") as f:
                errors = json.load(f)
            with open(os.path.join(run_dir, "data.csv"), "r") as f:
                reader = csv.reader(f)
                data = [",".join(row) for row in reader]
            with open(os.path.join(run_dir, "printouts.txt"), "r") as f:
                printouts = f.readlines()

            c = CsvPath()
            c.variables = variables
            c.metadata = meta["metadata"]
            c.identity = meta["identity"]
            result = Result(
                lines=data,
                csvpath=c,
                file_name=meta["file_name"],
                paths_name=meta["paths_name"],
                run_index=meta["run_index"],
                run_time=meta["run_time"],
                runtime_data=meta["runtime_data"],
            )
            result.errors = errors
            result.set_printouts("all", printouts)

            return result
        except (FileNotFoundError, ValueError, IOError):
            return None
    """
