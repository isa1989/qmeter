from django.views.generic import TemplateView

from .aggregation import MongoAggregation


class FeedbackRateView(TemplateView):
    template_name = "feedback_rate.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        mongo_aggregation = MongoAggregation()
        data = mongo_aggregation.calculate_feedback_rate()

        for branch in data:
            for service in branch["services"]:
                rating_1 = service["rating_1"]
                rating_2 = service["rating_2"]
                rating_3 = service["rating_3"]
                rating_4 = service["rating_4"]
                rating_5 = service["rating_5"]

                total_ratings = rating_1 + rating_2 + rating_3 + rating_4 + rating_5

                score = (
                    100
                    * (
                        rating_1 * 10
                        + rating_2 * 5
                        + rating_3 * 0
                        + rating_4 * -5
                        + rating_5 * -10
                    )
                ) / (total_ratings * 10)

                service["pythonic"] = score

        context["data"] = data
        return context
