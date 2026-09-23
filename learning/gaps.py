from learning.models import Lesson, LearningProfile


class KnowledgeGapDetector:

    def detect(
        self,
        lessons: list[Lesson],
        profile: LearningProfile,
    ) -> list[str]:

        gaps = []

        for lesson in lessons:

            if lesson.needs_revision:
                gaps.append(
                    lesson.topic.name
                )
                continue

            if lesson.total_answers > 0:

                accuracy = (
                    lesson.correct_answers
                    / lesson.total_answers
                )

                if accuracy < 0.70:
                    gaps.append(
                        lesson.topic.name
                    )

        for gap in gaps:
            profile.weak_areas[gap] = 1.0
            profile.difficult_concepts.add(gap)
            profile.revision_topics.add(gap)

        return gaps
