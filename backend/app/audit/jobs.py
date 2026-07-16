import uuid
from datetime import datetime
from typing import List, Optional
import structlog

logger = structlog.get_logger()


class BackgroundJobStore:
    def __init__(self):
        self._jobs: dict = {}

    def submit(self, job_type: str, name: str, payload: dict = None) -> dict:
        job_id = uuid.uuid4().hex[:12]
        job = {
            "id": job_id,
            "type": job_type,
            "name": name,
            "payload": payload or {},
            "status": "queued",
            "progress": 0,
            "result": None,
            "error": None,
            "created_at": datetime.now().isoformat(),
            "started_at": None,
            "completed_at": None,
        }
        self._jobs[job_id] = job
        return job

    def start(self, job_id: str) -> bool:
        job = self._jobs.get(job_id)
        if job and job["status"] == "queued":
            job["status"] = "running"
            job["started_at"] = datetime.now().isoformat()
            return True
        return False

    def complete(self, job_id: str, result: dict = None) -> bool:
        job = self._jobs.get(job_id)
        if job:
            job["status"] = "completed"
            job["progress"] = 100
            job["result"] = result
            job["completed_at"] = datetime.now().isoformat()
            return True
        return False

    def fail(self, job_id: str, error: str) -> bool:
        job = self._jobs.get(job_id)
        if job:
            job["status"] = "failed"
            job["error"] = error
            job["completed_at"] = datetime.now().isoformat()
            return True
        return False

    def get_job(self, job_id: str) -> Optional[dict]:
        return self._jobs.get(job_id)

    def list_jobs(self, status: str = None, limit: int = 50) -> List[dict]:
        jobs = list(self._jobs.values())
        if status:
            jobs = [j for j in jobs if j["status"] == status]
        return list(reversed(jobs))[:limit]

    def get_stats(self) -> dict:
        total = len(self._jobs)
        queued = sum(1 for j in self._jobs.values() if j["status"] == "queued")
        running = sum(1 for j in self._jobs.values() if j["status"] == "running")
        completed = sum(1 for j in self._jobs.values() if j["status"] == "completed")
        failed = sum(1 for j in self._jobs.values() if j["status"] == "failed")
        return {"total": total, "queued": queued, "running": running,
                "completed": completed, "failed": failed}
