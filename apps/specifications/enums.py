from django.db import models


class SpecificationPhase(models.IntegerChoices):
    PLANNING = 1, "Planning"
    PLANNING_READY = 2, "PlanningReady"
    DESIGN = 3, "Design"
    DESIGN_READY = 4, "DesignReady"
    BUILDING = 5, "Building"
    BUILT = 6, "Built"

    @classmethod
    def clone_ready_choices(cls) -> set["SpecificationPhase"]:
        return {
            cls.PLANNING_READY,
            cls.DESIGN,
            cls.DESIGN_READY,
            cls.BUILDING,
            cls.BUILT,
        }
