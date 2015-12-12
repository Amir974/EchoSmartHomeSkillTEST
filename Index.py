"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function


def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])


def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "SetTempIntent":
        return set_temp_in_session(intent, session)
    elif intent_name == "WhatsTempIntent":
        return get_status_from_session(intent, session)
    elif intent_name == "ShutdownIntent":
        return set_shutdown(intent, session)		
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here

# --------------- Functions that control the skill's behavior ------------------


def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to Smart Home app. " \
                    "What would you like to do?" 
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please let me know what you want me to do by saying, " \
                    "what's the current temperature, or set 24 hot or shut down"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def set_temp_in_session(intent, session):
    """ Sets the temprature in the session and prepares the speech to reply to the
    user.
    """

    card_title = intent['name']
    session_attributes = {}
    should_end_session = False
    
    """    
    test_status = 'value' in intent['slots']['FanSpeed']
    print("fan speed slot state:")
    print(test_status)
    test_status = 'value' in intent['slots']['Temprature']
    print("Temprature slot state:")
    print(test_status)
    """
    print("****")
    print(intent['slots'])
    print("****")

    if 'value' in intent['slots']['FanSpeed']:
        requested_fan_speed = intent['slots']['FanSpeed']['value']
    else:
        requested_fan_speed = "1"
	
    if 'value' in intent['slots']['ActionType'] and 'value' in intent['slots']['Temprature']:
        requested_action = intent['slots']['ActionType']['value']
        requested_temprature = intent['slots']['Temprature']['value']
		
        session_attributes = create_favorite_action_attributes(requested_action,requested_temprature,requested_fan_speed)
		
        speech_output = "I understand you want to set action to: " + \
                        requested_action + \
                        ". Temperature to:" + \
                        requested_temprature + \
                        ". And fan speed to:" + \
						requested_fan_speed + \
                        ". I will try to do that now..."
        reprompt_text = "Please let me know what you want me to do by saying, " \
						"what's the current temperature, or set 24 hot or shut down"
    else:
        speech_output = "I'm not sure what you wanted me to do. " \
                        "Please try again."
        reprompt_text = "I'm not sure what you wanted me to do. " \
                        "Please let me know by saying, " \
						"what's set 24 hot or something"
						
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def create_favorite_action_attributes(requested_action,requested_temprature,requested_fan_speed):
    return {"requested_action": requested_action,
		"requested_temprature": requested_temprature,
		"requested_fan_speed": requested_fan_speed}


def get_status_from_session(intent, session):
    session_attributes = {}
    reprompt_text = None
    
    speech_output = "I haven't learned how to check that yet"
    should_end_session = True

    # Setting reprompt_text to None signifies that we do not want to reprompt
    # the user. If the user does not respond or says something that is not
    # understood, the session will end.
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))

def set_shutdown(intent, session):
	session_attributes = {}
	reprompt_text = None
	speech_output = "I will try to shut the AC down now"
	should_end_session = True

	# Setting reprompt_text to None signifies that we do not want to reprompt
	# the user. If the user does not respond or says something that is not
	# understood, the session will end.
	return build_response(session_attributes, build_speechlet_response(
		intent['name'], speech_output, reprompt_text, should_end_session))		
# --------------- Helpers that build all of the responses ----------------------


def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': 'SessionSpeechlet - ' + title,
            'content': 'SessionSpeechlet - ' + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }