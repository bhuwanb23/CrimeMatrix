import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
import structlog

logger = structlog.get_logger()


class ReportQueue:
    def __init__(self):
        self._queue: Dict[str, Dict] = {}

    def submit(self, report_type: str, params: dict, template_id: str = None) -> Dict[str, Any]:
        job_id = uuid.uuid4().hex[:12]
        job = {
            "id": job_id,
            "type": report_type,
            "template_id": template_id,
            "params": params,
            "status": "queued",
            "created_at": datetime.now().isoformat(),
            "started_at": None,
            "completed_at": None,
            "result": None,
            "error": None,
        }
        self._queue[job_id] = job
        logger.info("report_queued", job_id=job_id, type=report_type)
        return job

    def list_jobs(self) -> List[Dict]:
        return list(self._queue.values())

    def get_job(self, job_id: str) -> Optional[Dict]:
        return self._queue.get(job_id)

    def update_status(self, job_id: str, status: str, result: str = None, error: str = None):
        if job_id in self._queue:
            self._queue[job_id]["status"] = status
            if status == "processing":
                self._queue[job_id]["started_at"] = datetime.now().isoformat()
            elif status in ("completed", "failed"):
                self._queue[job_id]["completed_at"] = datetime.now().isoformat()
            if result:
                self._queue[job_id]["result"] = result
            if error:
                self._queue[job_id]["error"] = error

    def cancel(self, job_id: str) -> bool:
        if job_id in self._queue and self._queue[job_id]["status"] == "queued":
            self._queue[job_id]["status"] = "cancelled"
            return True
        return False
