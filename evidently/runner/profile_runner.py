import json
from dataclasses import dataclass
from typing import List

from evidently.model_profile import Profile
from evidently.profile_sections.data_drift_profile_section import DataDriftProfileSection 
from evidently.profile_sections.cat_target_drift_profile_section import CatTargetDriftProfileSection
from evidently.profile_sections.num_target_drift_profile_section import NumTargetDriftProfileSection
from evidently.profile_sections.classification_performance_profile_section import ClassificationPerformanceProfileSection
from evidently.profile_sections.prob_classification_performance_profile_section import ProbClassificationPerformanceProfileSection
from evidently.profile_sections.regression_performance_profile_section import RegressionPerformanceProfileSection
from evidently.runner.runner import RunnerOptions, Runner


@dataclass
class ProfileRunnerOptions(RunnerOptions):
    profile_parts: List[str]
    pretty_print: bool

parts_mapping = dict(
    data_drift=DataDriftProfileSection,
    cat_target_drift=CatTargetDriftProfileSection,
    classification_performance=ClassificationPerformanceProfileSection,
    prob_classification_performance=ProbClassificationPerformanceProfileSection,
    num_target_drift=NumTargetDriftProfileSection,
    regression_performance=RegressionPerformanceProfileSection,

)

class ProfileRunner(Runner):
    def __init__(self, options: ProfileRunnerOptions):
        super().__init__(options)
        self.options = options

    def run(self):
        (reference_data, production_data) = self._parse_data()

        parts = []

        for part in self.options.profile_parts:
            part_class = parts_mapping.get(part, None)
            if part_class is None:
                raise ValueError(f"Unknown profile section {part}")
            parts.append(part_class)

        profile = Profile(sections=parts)
        profile.calculate(reference_data, production_data, self.options.column_mapping)
        output_path = self.options.output_path \
            if self.options.output_path.endswith(".json") \
            else self.options.output_path + ".json"

        with open(output_path, 'w') as f:
            json.dump(profile.object(), f, indent=2 if self.options.pretty_print else None)
