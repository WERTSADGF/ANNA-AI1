from learning.models import (
    Lesson,
    LearningProfile,
)


class ProgressTracker:

    def update(
        self,
        lesson: Lesson,
        profile: LearningProfile,
    ) -> LearningProfile:

        topic = lesson.topic.name

        if lesson.total_answers == 0:
            progress = 0.0
        else:
            progress = (
                lesson.correct_answers
                / lesson.total_answers
            )

        profile.progress_by_topic[
            topic
        ] = progress

        if (
            lesson.state.value == "completed"
            and progress >= 0.80
        ):
            profile.completed_topics.add(
                topic
            )

        if progress >= 0.80:
            profile.strong_areas[topic] = progress

        if progress < 0.70 and lesson.total_answers > 0:
            profile.weak_areas[topic] = progress
            profile.revision_topics.add(topic)

        return profile
