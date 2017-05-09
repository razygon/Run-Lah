"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function
import googlemaps
import datetime
import json
import requests

mrt_parks = {'BOON KENG MRT': [['KALLANG PARK CONNECTOR', '', '1', '0', '0', '1']], 'KENT RIDGE MRT': [['RUNNING AT NUS CAMPUS', '', '1', '1', '0', '1'], ['SOUTH BUONA VISTA ROAD', '', '1', '0', '0', '1']], 'MARINA BAY MRT': [['LAZARUS ISLAND', '', '1', '1', '1', '0']], 'HOUGANG MRT': [['PUNGGOL PARK', '', '1', '1', '0', '1']], 'CHINESE GARDEN MRT': [['JURONG PARK CONNECTOR', '', '0', '1', '1', '1']], 'CLARKE QUAY MRT': [['FORT CANNING PARK', '', '1', '0', '0', '1']], 'CALDECOTT MRT': [['MACRITCHIE RESERVOIR', '', '0', '1', '1', '1']], 'KALLANG MRT': [['KALLANG RIVERSIDE PARK', '', '1', '1', '0', '1']], 'KHATIB MRT': [['MANDAI ROAD', '', '1', '0', '0', '1']], 'LAVENDER MRT': [['KALLANG RIVERSIDE PARK', '', '1', '1', '0', '1']], 'DAKOTA MRT': [['GEYLANG RIVER', '', '1', '1', '0', '1']], 'STADIUM MRT. ': [['100PLUS PROMENADE', '', '1', '0', '0', '1']], 'PUBLIC TRANSPORTATION': [['ROUTE_NAME', 'ADDRESS', 'SHORT', 'MEDIUM', 'LONG', 'NIGHT']], 'QUEENSTOWN MRT': [['ALEXANDRA CANAL LINEAR PARK', '', '1', '0', '0', '1'], ['SINGAPORE RIVER', '', '0', '1', '1', '1']], 'BISHAN MRT': [['BISHAN ANG MO KIO PARK', '', '1', '1', '0', '1']], 'DHOBY GHAUT MRT': [['FORT CANNING PARK', '', '1', '0', '0', '1']], 'TANAH MERAH MRT': [['PULAU UBIN', '', '0', '1', '1', '0']], 'BUONA VISTA MRT': [['ONE NORTH PARK', '', '1', '1', '0', '1'], ['ULU PANDAN PARK CONNECTOR', '', '0', '1', '0', '1']], 'PROMENADE MRT': [['BENJAMIN SHEARES BRIDGE', '', '1', '0', '0', '1']], 'CHOA CHU KANG MRT': [['CHESTNUT NATURE PARK', '', '1', '0', '0', '0']], 'BUKIT GOMBAK MRT': [['BUKIT BATOK TOWN PARK LITTLE GUILIN', '', '1', '0', '0', '0']], 'SEMBAWANG MRT': [['SEMBAWANG PARK', '', '1', '1', '0', '0']], 'BOTANIC GARDENS MRT': [['ARCADIA ROAD', '', '1', '0', '0', '1'], ['MOE CO CURRICULAR ACTIVITIES STADIUM CCAB EVANS', '', '1', '1', '0', '1']], 'WOODLANDS MRT': [['ADMIRALTY PARK', '', '1', '1', '0', '1']], 'RAFFLES PLACE MRT': [['MARINA BAY', '', '1', '1', '0', '1']], 'JURONG EAST MRT': [['TOH GUAN PARK', '', '1', '0', '0', '1']], 'CITY HALL MRT': [['ESPLANADE PARK', '', '1', '1', '0', '1']], 'LAKESIDE MRT': [['JURONG LAKE PARK', '', '0', '1', '0', '1']], 'TIONG BAHRU MRT': [['TIONG BAHRU PARK', '', '1', '0', '0', '1']], 'BAYFRONT MRT': [['FORT ROAD NEW RUNNING ROUTE IN SINGAPORE', '', '0', '1', '0', '1'], ['MARINA BAY', '', '1', '1', '0', '1']], 'DOVER MRT': [['CLEMENTI WOODS PARK', '', '1', '0', '0', '1']], 'BUANGKOK MRT': [['PUNGGOL PARK', '', '1', '1', '0', '1']], 'LABRADOR PARK MRT': [['LABRADOR NATURE RESERVE', '', '0', '1', '0', '0']], 'PUNGGOL MRT': [['PUNGGOL WATERWAY PARK', '', '1', '1', '1', '1']], 'TOA PAYOH MRT': [['CENTRAL URBAN LOOP PARK CONNECTOR', '', '0', '0', '1', '1'], ['TOA PAYOH TOWN PARK', '', '1', '0', '0', '1']], 'TAMPINES MRT': [['TAMPINES ECO GREEN', '', '1', '1', '1', '0']], 'PASIR RIS MRT': [['PASIR RIS PARK', '', '1', '1', '1', '1'], ['TAMPINES ECO GREEN', '', '1', '1', '1', '0']], 'YISHUN MRT': [['YISHUN NEIGHBOURHOOD PARK', '', '1', '0', '0', '1'], ['YISHUN PARK', '', '1', '1', '0', '1'], ['YISHUN POND PARK', '', '1', '1', '0', '1']], 'RAFFLES PLACE MRT ': [['SINGAPORE RIVER', '', '0', '1', '1', '1']], 'MOUNTBATTEN MRT': [['EAST COAST PARK', '', '1', '1', '1', '1'], ['FORT ROAD NEW RUNNING ROUTE IN SINGAPORE', '', '0', '1', '0', '1']], 'ANG MO KIO MRT': [['ANG MO KIO TOWN GARDEN EAST', '', '1', '0', '0', '1'], ['ANG MO KIO TOWN GARDEN WEST', '', '1', '1', '0', '1']], 'BOON LAY MRT': [['JURONG CENTRAL PARK', '', '1', '0', '0', '1']]}
 
# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
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


# --------------- Functions that control the skill's behavior ------------------


def get_cancel_response(intent, session):
    """Response given when the user cancels the skill"""
    card_title = "Goodbye"
    session_attributes = session.get('attributes', {})
    
    should_end_session = True
    speech_output = "OK, goodbye"
    reprompt_text = None
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def error_response(intent, session):
    """Response given when an unexpected error occurs"""
    card_title = "Oops"
    session_attributes = session.get('attributes', {})
    should_end_session = False
    speech_output = "Sorry, I didn't understand what you said. " \
                    "Please try again."
    reprompt_text = speech_output
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def distance_not_found(intent, session, distance, mrt):
    """
    Response given when the distance is not found in the
    predefined data.
    """
    card_title = "Distance Not Found"
    session_attributes = session.get('attributes', {})
    should_end_session = False
    speech_output = "Sorry, I couldn't find route that match the distance, {}, near {}. " \
                    "Please try again.".format(distance, mrt)
    reprompt_text = "Sorry, I didn't understand what you said. " \
                    "Please try again."
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def mrt_not_found(intent, session, distance, location):
    """
    Response given when the name of the location is not found in the
    predefined data.
    """
    card_title = "location Not Found"
    session_attributes = session.get('attributes', {})
    should_end_session = False
    speech_output = "Sorry, I couldn't find the {} route near {}. " \
                    "Please try again.".format(distance, mrt)
    reprompt_text = "Sorry, I didn't understand what you said. " \
                    "Please try again."
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Hello, I can recomend a jogging route for you by saying" \
                    "I would like to run 5km near botanic garden. "\

    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Sorry, I didn't understand what you said. " \
                    "Please tell me how long you would like to run near which MRT station"\
                    "For example, you can say, " \
                    " I would like to go for 5km run near bishan"

    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "The plan is done! Enjoy! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

def get_park(mrt):
    mrtstation = mrt + ' MRT'
    if mrtstation.upper() in mrt_parks:
        return mrt_parks[mrtstation.upper()][0][0]
    else:
        return mrt+" park"

def get_parks(mrt):
    mrtstation = mrt + ' MRT'
    parks= ''
    if mrtstation.upper() in mrt_parks:
        for item in mrt_parks[mrtstation.upper()]:
            parks += item[0]
        return parks
    else:
        return None

def get_time_cost(dest_addr):
    GMAPS_API_KEY = "AIzaSyDgeLCSft_WLxdhbbGB1ZgQveRVL2ARySU"
    APP_ID = "amzn1.ask.skill.11e96892-b8e5-40f2-b936-5c1f59bb0dd9"
    gmaps = googlemaps.Client(key=GMAPS_API_KEY)
    departure_time = datetime.datetime.now()
    start_addr = "21 Church Street, Singapore"
    print(start_addr, dest_addr)
    res = gmaps.directions(start_addr, dest_addr,mode="transit",departure_time=departure_time)
    mins = res[0]['legs'][0]['duration']['text']
    return mins

def get_weather(location):
    url = 'http://api.openweathermap.org/data/2.5/weather?q='+ location +',SG&APPID=5dac6da5acc2b0ed28e51bd28553bbb5'
    r = requests.get(url)
    data = r.text
    data_parsed = json.loads(data)
    if 'wind' in data_parsed:
        data_parsed['wind']['speed']
        return (data_parsed['weather'][0]['main'] ,data_parsed['wind']['speed'])
    return (data_parsed['weather'][0]['main'] , '')


def set_distance_in_session(intent, session):
    """ Sets the distance in the session and prepares the speech to reply to the
    user.
    """

    card_title = intent['name']
    session_attributes = {}
    should_end_session = False
    reprompt_text = ""
    # if 'Distance' in intent['slots']:
    if 'value' in intent['slots']['Distance']:
        Running_Distance = intent['slots']['Distance']['value']
        session_attributes["RunningDistance"] = Running_Distance
        speech_output = "I now know your running distance is " + \
                        Running_Distance 

    else:
        speech_output = "tell me how long you plan to run!"
        reprompt_text = "reprompt, tell me how long you plan to run!"
    # if 'Mrt' in intent['slots']:
    if 'value' in  intent['slots']['Mrt']:
        MRT_Station = intent['slots']['Mrt']['value']
        session_attributes["MRTStation"] = MRT_Station
        speech_output += "Your target MRT is " + \
                        MRT_Station 
        Running_Park = get_park(MRT_Station)
        session_attributes["Park"] = Running_Park

    else:
        speech_output += " tell me the destination MRT!"
        reprompt_text += " tell me the destination MRT!"
    
        
    # build_response(session_attributes, {})
    if 'attributes' in session:
        session['attributes'].update(session_attributes)
    else:
        session['attributes'] = session_attributes

    if session.get('attributes', {}) and "RunningDistance" in session.get('attributes', {}) \
                                    and "MRTStation" in session.get('attributes', {})\
                                    and "Park" in session.get('attributes', {}):
    #     if  "RunningDistance" in session_attributes and "MRTStation" in session_attributes:

        Running_Distance = session['attributes']['RunningDistance']
        MRT_Station = session['attributes']['MRTStation']
        Running_Park = session['attributes']['Park']
        print('park:',Running_Park)
        Travel_time = get_time_cost(Running_Park)
        print('time:',Travel_time)
        weather, windy = get_weather(Running_Park)
        if weather == '' or weather == None:
            weather = "couldy"
        # Running_Time = "7"
        # Running_weather = "cloudy"
        # Travel_info = " "
        speech_output = "You can jog at "+ Running_Park +" for a " + Running_Distance + \
                        " Kilometers run " \
                        ". You can take the MRT to get there, travel time will be " + Travel_time + \
                        "The weather now is "+weather+". When you plan to run?"
        should_end_session = False

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))



# --------------- Events ------------------

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

def set_stop(intent,session):
    should_end_session = True
    card_title = intent['name']
    speech_output = "Goodbye, do plan a run next time!"
    return build_response({}, build_speechlet_response(
        card_title, speech_output, '', should_end_session))

def running_rountes(intent, session):
    should_end_session = False
    card_title = intent['name']
    speech_output = ""
    mrt = intent['slots']['Mrt']['value']
    parks = get_parks(mrt)
    if parks:
        speech_output +=parks
    else:
        speech_output = "Sorry, there is no running place near " + mrt 
    return build_response({}, build_speechlet_response(
        card_title, speech_output, '', should_end_session))

def start_time(intent,session):
    should_end_session = True
    card_title = intent['name']
    speech_output = ""
    time = intent['slots']['Time']['value']
    location = session['attributes']['Park']
    print(time,location)
    weather, windy = get_weather(location)
    print(weather,windy)
    if "RAIN" in weather.upper() or weather.upper() == "THUNDERSTORM":
        speech_output = "It's raining there, you should better take a rest, maybe run tomorrow!"
        return build_response({}, build_speechlet_response(
        card_title, speech_output, '', should_end_session))
    if weather:
        speech_output = "The weather at " + location + " is " + weather
    if windy:
        speech_output += "The wind speed is " + str(windy) +". Enjoy!"
    else:
        speech_output = "Sorry, there is no running place near " + mrt 
    return build_response({}, build_speechlet_response(
        card_title, speech_output, '', should_end_session))

def all_running_rountes(intent, session):
    parks = ["100plus promenade", "admiralty park",
"alexandra canal linear park",
"ang mo kio town garden east",
"ang mo kio town garden west",
"arcadia road",
"benjamin sheares bridge",
"bishan ang mo kio park",
"bukit batok town park little guilin",
"central urban loop park connector",
"chestnut nature park",
"clementi woods park",
"east coast park",
"esplanade park",
"fort canning park",
"fort road new running route in singapore",
"geylang river",
"jurong central park",
"jurong lake park",
"jurong park connector",
"kallang park connector",
"kallang riverside park",
"labrador nature reserve",
"lazarus island",
"macritchie reservoir",
"mandai road",
"marina bay",
"moe co curricular activities stadium ccab evans",
"running at nus campus",
"one north park",
"pasir ris park",
"pulau ubin",
"punggol park",
"punggol waterway park",
"sembawang park",
"singapore river",
"south buona vista road",
"tampines eco green",
"tiong bahru park",
"toa payoh town park",
"toh guan park",
"ulu pandan park connector",
"yishun neighbourhood park",
"yishun park",
"yishun pond park"]
    should_end_session = False
    card_title = intent['name']
    speech_output = ""
    for item in parks:
        speech_output +=item
    return build_response({}, build_speechlet_response(
        card_title, speech_output, '', should_end_session))


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers

    # print type(intent_name)
    if intent_name == "GiveRoutesIntent":
        return set_distance_in_session(intent, session)
    elif intent_name == "StopIntent":
        return set_stop(intent,session)
    elif intent_name == "StartTimeIntent":
        return start_time(intent,session)
    elif intent_name == "ListRouteIntent":
        return running_rountes(intent,session)
    elif intent_name == "ListAllRouteIntent":
        return all_running_rountes(intent,session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

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
