import logging
from get_discussion import *
import json

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler, AbstractExceptionHandler,
    AbstractRequestInterceptor, AbstractResponseInterceptor)
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.serialize import DefaultSerializer

from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response

SKILL_NAME = 'NWS Forecast Discussion'
HELP_MESSAGE = '''To hear a forecast discussion, say something like \'Alexa, ask
    Forecast Discussion for the discussion in Seattle\'. You can also ask for 
    the short term discussion, long term discussion, or synopsis.'''
STOP_MESSAGE = ''
FALLBACK_MESSAGE = 'I\'m sorry, I could not understand the request. ' + HELP_MESSAGE
EXCEPTION_MESSAGE = 'Sorry, something went wrong.'
OFFICE_NOT_FOUND = 'No forecast office found in {}. Visit www.spc.noaa.gov/misc/NWS_WFO_ID.txt to find a list of valid cities.'
GET_CITY_TEXT = 'The forecast discussion is fetched from weather forecast offices in the United States. Which city would you like the forecast discussion for?'

sb = SkillBuilder()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class LaunchForecastDiscussionHandler(AbstractRequestHandler):
    """Handler for LaunchForecastDiscussion Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In LaunchForecastDiscussionHandler")
        (handler_input.response_builder.speak(GET_CITY_TEXT)
                                       .ask(GET_CITY_TEXT)
                                       .set_card(SimpleCard(SKILL_NAME, GET_CITY_TEXT)))

        return handler_input.response_builder.response

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

        try:
            text = get_forecast_discussion(city)
            speech_output = 'FORECAST DISCUSSION FOR {}. '.format(city.upper()) + text
        except OfficeNotFoundError:
            speech_output = OFFICE_NOT_FOUND.format(city)

        (handler_input.response_builder.speak(speech_output)
                                       .ask(speech_output)
                                       .set_card(SimpleCard(SKILL_NAME, speech_output)))

        return handler_input.response_builder.response

class ShortTermDiscussionHandler(AbstractRequestHandler):
    """Handler for ShortTermDiscussion Intent."""
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
                                       .ask(speech_output)
                                       .set_card(SimpleCard(SKILL_NAME, speech_output)))

        return handler_input.response_builder.response

class LongTermDiscussionHandler(AbstractRequestHandler):
    """Handler for LongTermDiscussion Intent."""
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
                                       .ask(speech_output)
                                       .set_card(SimpleCard(SKILL_NAME, speech_output)))

        return handler_input.response_builder.response

class SynopsisHandler(AbstractRequestHandler):
    """Handler for Synopsis Intent."""
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
                                       .ask(speech_output)
                                       .set_card(SimpleCard(SKILL_NAME, speech_output)))

        return handler_input.response_builder.response

class ForecastUpdateHandler(AbstractRequestHandler):
    """Handler for ForecastUpdate Intent."""
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
                                       .ask(speech_output)
                                       .set_card(SimpleCard(SKILL_NAME, speech_output)))

        return handler_input.response_builder.response

# Built-in Intent Handlers
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

class RepeatHandler(AbstractRequestHandler):
    """Handler for repeating the response to the user."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.RepeatIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In RepeatHandler")
        attr = handler_input.attributes_manager.session_attributes
        response_builder = handler_input.response_builder
        if "recent_response" in attr:
            cached_response_str = json.dumps(attr["recent_response"])
            cached_response = DefaultSerializer().deserialize(
                cached_response_str, Response)
            return cached_response
        else:
            response_builder.speak(data.FALLBACK_ANSWER).ask(data.HELP_MESSAGE)

            return response_builder.response


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
        logger.info(handler_input.request_envelope.request)

        handler_input.response_builder.speak(EXCEPTION_MESSAGE)

        return handler_input.response_builder.response

# Interceptor classes
class CacheResponseForRepeatInterceptor(AbstractResponseInterceptor):
    """Cache the response sent to the user in session.
    The interceptor is used to cache the handler response that is
    being sent to the user. This can be used to repeat the response
    back to the user, in case a RepeatIntent is being used and the
    skill developer wants to repeat the same information back to
    the user.
    """
    def process(self, handler_input, response):
        # type: (HandlerInput, Response) -> None
        session_attr = handler_input.attributes_manager.session_attributes
        session_attr["recent_response"] = response

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
sb.add_request_handler(LaunchForecastDiscussionHandler())
sb.add_request_handler(ForecastDiscussionHandler())
sb.add_request_handler(ShortTermDiscussionHandler())
sb.add_request_handler(LongTermDiscussionHandler())
sb.add_request_handler(SynopsisHandler())
sb.add_request_handler(ForecastUpdateHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(RepeatHandler())

# Register exception handlers
sb.add_exception_handler(CatchAllExceptionHandler())

# Register request and response interceptors
sb.add_global_response_interceptor(CacheResponseForRepeatInterceptor())
sb.add_global_request_interceptor(RequestLogger())
sb.add_global_response_interceptor(ResponseLogger())

# Handler name that is used on AWS lambda
lambda_handler = sb.lambda_handler()
