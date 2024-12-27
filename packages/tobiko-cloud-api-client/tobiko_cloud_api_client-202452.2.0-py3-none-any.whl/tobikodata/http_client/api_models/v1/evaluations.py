import typing as t
from datetime import datetime

from pydantic import BaseModel, HttpUrl

from tobikodata.http_client.api_models.v1.common import V1Status


class V1EvaluationBase(BaseModel):
    evaluation_id: str
    node_name: str
    start_at: t.Optional[datetime]
    end_at: t.Optional[datetime]
    error_message: t.Optional[str]
    log: t.Optional[str]
    status: V1Status
    link: HttpUrl
    log_link: HttpUrl

    @property
    def complete(self) -> bool:
        return self.status.complete


class V1PlanEvaluation(V1EvaluationBase):
    plan_id: str


class V1RunEvaluation(V1EvaluationBase):
    run_id: str


V1Evaluation = t.Union[V1PlanEvaluation, V1RunEvaluation]
