import json
import logging
from pathlib import Path
from typing import Any

import pandas as pd

from nxbench.benchmarks.config import BenchmarkResult
from nxbench.benchmarks.utils import get_python_version
from nxbench.data.db import BenchmarkDB
from nxbench.data.loader import BenchmarkDataManager

logger = logging.getLogger("nxbench")


class ResultsExporter:
    """Handle loading, processing, and exporting of benchmark results."""

    def __init__(self, results_file: Path):
        """Initialize the results exporter.

        Parameters
        ----------
        results_file : Path
            Path to the benchmark results file (JSON or CSV)
        """
        self.results_file = results_file
        self.data_manager = BenchmarkDataManager()
        self._cached_results: list[BenchmarkResult] | None = None

    def load_results(self) -> list[BenchmarkResult]:
        """Load benchmark results from the workflow outputs (JSON or CSV),
        integrating all known fields into BenchmarkResult and treating unknown
        fields as metadata.
        """
        if self._cached_results is not None:
            return self._cached_results

        results = []

        try:
            if self.results_file.suffix.lower() == ".json":
                with self.results_file.open("r") as f:
                    data = json.load(f)
                if not isinstance(data, list):
                    logger.error(
                        f"Expected a list of results in JSON file, got {type(data)}"
                    )
                    return []

                for entry in data:
                    result = self._create_benchmark_result_from_entry(entry)
                    if result:
                        results.append(result)

            elif self.results_file.suffix.lower() == ".csv":
                df = pd.read_csv(self.results_file)
                for _, row in df.iterrows():
                    entry = row.to_dict()
                    result = self._create_benchmark_result_from_entry(entry)
                    if result:
                        results.append(result)
            else:
                logger.error(f"Unsupported file format: {self.results_file.suffix}")
                return []

        except Exception:
            logger.exception(f"Failed to load results from: {self.results_file}")
            return []

        self._cached_results = results
        logger.info(f"Loaded {len(results)} benchmark results from {self.results_file}")
        return results

    def _create_benchmark_result_from_entry(
        self, entry: dict[str, Any]
    ) -> BenchmarkResult | None:
        try:
            known_fields = {
                "algorithm",
                "dataset",
                "execution_time",
                "execution_time_with_preloading",
                "memory_used",
                "num_nodes",
                "num_edges",
                "is_directed",
                "is_weighted",
                "backend",
                "num_thread",
                "date",
                "validation",
                "validation_message",
                "error",
            }

            algorithm = entry.get("algorithm", "unknown")
            dataset = entry.get("dataset", "unknown")
            backend = entry.get("backend", "unknown")
            execution_time = float(entry.get("execution_time", float("nan")))
            execution_time_with_preloading = float(
                entry.get("execution_time_with_preloading", float("nan"))
            )
            memory_used = float(entry.get("memory_used", float("nan")))
            num_thread = int(entry.get("num_thread", 1))
            num_nodes = int(entry.get("num_nodes", 0))
            num_edges = int(entry.get("num_edges", 0))
            is_directed = bool(entry.get("is_directed", False))
            is_weighted = bool(entry.get("is_weighted", False))
            date = int(entry.get("date", 0))
            validation = entry.get("validation", "unknown")
            validation_message = entry.get("validation_message", "")
            error = entry.get("error")

            metadata = {k: v for k, v in entry.items() if k not in known_fields}

            return BenchmarkResult(
                algorithm=algorithm,
                dataset=dataset,
                execution_time=execution_time,
                execution_time_with_preloading=execution_time_with_preloading,
                memory_used=memory_used,
                num_nodes=num_nodes,
                num_edges=num_edges,
                is_directed=is_directed,
                is_weighted=is_weighted,
                backend=backend,
                num_thread=num_thread,
                date=date,
                metadata=metadata,
                validation=validation,
                validation_message=validation_message,
                error=error,
            )
        except Exception:
            logger.exception("Failed to process result entry.")
            return None

    def to_dataframe(self) -> pd.DataFrame:
        results = self.load_results()
        if not results:
            raise ValueError("No benchmark results found")

        records = []
        all_metadata_keys = set()

        for result in results:
            record = {
                "algorithm": result.algorithm,
                "dataset": result.dataset,
                "backend": result.backend,
                "execution_time": result.execution_time,
                ### ADDED:
                "execution_time_with_preloading": result.execution_time_with_preloading,
                ### END ADDED
                "memory_used": result.memory_used,
                "num_nodes": result.num_nodes,
                "num_edges": result.num_edges,
                "is_directed": result.is_directed,
                "is_weighted": result.is_weighted,
                "num_thread": result.num_thread,
                "date": result.date,
                "validation": result.validation,
                "validation_message": result.validation_message,
                "error": result.error,
                "python_version": get_python_version(),
            }

            for k, v in result.metadata.items():
                record[k] = v
                all_metadata_keys.add(k)

            records.append(record)

        df = pd.DataFrame(records)
        for mk in all_metadata_keys:
            if mk not in df.columns:
                df[mk] = pd.NA

        return df

    def export_results(
        self, output_path: Path, form: str = "csv", if_exists: str = "replace"
    ) -> None:
        """Export benchmark results in specified format (csv, sql, json)."""
        df = self.to_dataframe()

        if form == "csv":
            df.to_csv(output_path, index=False)
            logger.info(f"Exported results to CSV: {output_path}")

        elif form == "sql":
            db = BenchmarkDB(output_path)

            if if_exists == "replace":
                db.delete_results()

            results = self.load_results()
            db.save_results(
                results=results,
                machine_info={},
                python_version=get_python_version(),
            )
            logger.info(f"Exported results to SQL database: {output_path}")

        elif form == "json":
            df.to_json(output_path, orient="records", indent=2)
            logger.info(f"Exported results to JSON: {output_path}")

        else:
            raise ValueError(f"Unsupported export format: {form}")

    def query_results(
        self,
        algorithm: str | None = None,
        backend: str | None = None,
        dataset: str | None = None,
        date_range: tuple[str, str] | None = None,
    ) -> pd.DataFrame:
        """Query benchmark results with optional filtering."""
        df = self.to_dataframe()

        if algorithm:
            df = df[df["algorithm"] == algorithm]
        if backend:
            df = df[df["backend"] == backend]
        if dataset:
            df = df[df["dataset"] == dataset]
        if date_range:
            start_date, end_date = date_range
            df = df[
                (df["date"] >= pd.to_datetime(start_date))
                & (df["date"] <= pd.to_datetime(end_date))
            ]

        return df.sort_values(["algorithm", "dataset", "backend"])
