import logging
from get_discussion import *

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler, AbstractExceptionHandler,
    AbstractRequestInterceptor, AbstractResponseInterceptor)
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response

SKILL_NAME = 'NWS Forecast Discussion'
HELP_MESSAGE = '''To hear a forecast discussion, say something like \'Alexa, ask
    Forecast Discussion for the discussion in Seattle\'. You can also ask for 
    the short term discussion, long term discussion, or synopsis.'''
STOP_MESSAGE = ''
FALLBACK_MESSAGE = 'I\'m sorry, I could not understand the request. ' + HELP_MESSAGE
EXCEPTION_MESSAGE = 'Sorry, something went wrong.'
OFFICE_NOT_FOUND = 'I\'m sorry, the office you requested could not be found.'

sb = SkillBuilder()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# Built-in Intent Handlers
class ForecastDiscussionHandler(AbstractRequestHandler):
    """Handler for ForecastDiscussion Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("ForecastDiscussionIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In ForecastDiscussionHandler")
        slots = handler_input.request_envelope.request.intent.slots
        city = str(slots['city'].value).lower()

        text = get_forecast_discussion(city)
        speech_output = OFFICE_NOT_FOUND if not text else 'FORECAST DISCUSSION FOR {}. '.format(city.upper()) + text

        (handler_input.response_builder.speak(speech_output)
                                       .set_card(SimpleCard(SKILL_NAME, speech_output)))

        return handler_input.response_builder.response

class ShortTermDiscussionHandler(AbstractRequestHandler):
    """Handler for ForecastDiscussion Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("ShortTermDiscussionIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In ShortTermDiscussionHandler")
        slots = handler_input.request_envelope.request.intent.slots
        city = str(slots['city'].value).lower()

        text = get_short_term_discussion(city)
        speech_output = OFFICE_NOT_FOUND if not text else 'SHORT TERM DISCUSSION FOR {}. '.format(city.upper()) + text

        (handler_input.response_builder.speak(speech_output)
                                       .set_card(SimpleCard(SKILL_NAME, speech_output)))

        return handler_input.response_builder.response

class LongTermDiscussionHandler(AbstractRequestHandler):
    """Handler for ForecastDiscussion Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("LongTermDiscussionIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In LongTermDiscussionHandler")
        slots = handler_input.request_envelope.request.intent.slots
        city = str(slots['city'].value).lower()

        text = get_long_term_discussion(city)
        speech_output = OFFICE_NOT_FOUND if not text else 'LONG TERM DISCUSSION FOR {}. '.format(city.upper()) + text

        (handler_input.response_builder.speak(speech_output)
                                       .set_card(SimpleCard(SKILL_NAME, speech_output)))

        return handler_input.response_builder.response

class SynopsisHandler(AbstractRequestHandler):
    """Handler for ForecastDiscussion Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("SynopsisIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In SynopsisHandler")
        slots = handler_input.request_envelope.request.intent.slots
        city = str(slots['city'].value).lower()

        text = get_synopsis(city)
        speech_output = OFFICE_NOT_FOUND if not text else 'SYNOPSIS FOR {}. '.format(city.upper()) + text

        (handler_input.response_builder.speak(speech_output)
                                       .set_card(SimpleCard(SKILL_NAME, speech_output)))

        return handler_input.response_builder.response

class ForecastUpdateHandler(AbstractRequestHandler):
    """Handler for ForecastDiscussion Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("ForecastUpdateIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In ForecastUpdateHandler")
        slots = handler_input.request_envelope.request.intent.slots
        city = str(slots['city'].value).lower()

        text = get_forecast_update(city)
        speech_output = OFFICE_NOT_FOUND if not text else 'FORECAST UPDATE FOR {}. '.format(city.upper()) + text

        (handler_input.response_builder.speak(speech_output)
                                       .set_card(SimpleCard(SKILL_NAME, speech_output)))

        return handler_input.response_builder.response

class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In HelpIntentHandler")

        speech = HELP_MESSAGE
        (handler_input.response_builder.speak(speech)
                                      .set_card(SimpleCard(SKILL_NAME, speech)))

        return handler_input.response_builder.response


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In CancelOrStopIntentHandler")

        speech = STOP_MESSAGE
        handler_input.response_builder.speak(speech)
        return handler_input.response_builder.response


class FallbackIntentHandler(AbstractRequestHandler):
    """Handler for Fallback Intent.
    AMAZON.FallbackIntent is only available in en-US locale.
    This handler will not be triggered except in that locale,
    so it is safe to deploy on any locale.
    """

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")

        speech = FALLBACK_MESSAGE
        handler_input.response_builder.speak(speech)
        return handler_input.response_builder.response

class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In SessionEndedRequestHandler")

        logger.info("Session ended reason: {}".format(
            handler_input.request_envelope.request.reason))
        return handler_input.response_builder.response


# Exception Handler
class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Catch all exception handler, log exception and
    respond with custom message.
    """

    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.info("In CatchAllExceptionHandler")
        logger.error(exception, exc_info=True)

        handler_input.response_builder.speak(EXCEPTION_MESSAGE)

        return handler_input.response_builder.response


# Request and Response loggers
class RequestLogger(AbstractRequestInterceptor):
    """Log the alexa requests."""

    def process(self, handler_input):
        # type: (HandlerInput) -> None
        logger.debug("Alexa Request: {}".format(
            handler_input.request_envelope.request))


class ResponseLogger(AbstractResponseInterceptor):
    """Log the alexa responses."""

    def process(self, handler_input, response):
        # type: (HandlerInput, Response) -> None
        logger.debug("Alexa Response: {}".format(response))


# Register intent handlers
sb.add_request_handler(ForecastDiscussionHandler())
sb.add_request_handler(ShortTermDiscussionHandler())
sb.add_request_handler(LongTermDiscussionHandler())
sb.add_request_handler(SynopsisHandler())
sb.add_request_handler(ForecastUpdateHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

# Register exception handlers
sb.add_exception_handler(CatchAllExceptionHandler())

# Register request and response interceptors
sb.add_global_request_interceptor(RequestLogger())
sb.add_global_response_interceptor(ResponseLogger())

# Handler name that is used on AWS lambda
lambda_handler = sb.lambda_handler()
