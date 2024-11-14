import os, base64
from openai import OpenAI

openai_api_key = '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'

def generate_narration(image_url):
    file_extension = os.path.splitext(image_url)[1].lower()
	
    if file_extension in ['.png', '.jpg', '.jpeg']:
        mime_type = f'image/{file_extension[1:]}'
    else:
        return 'Unsupported image type'

    base64_image = encode_image(image_url)
    image_url = f'data:image/{mime_type};base64,{base64_image}'
	
    prompt = f'''
        Generate notes for this slide. Don't use bullet points.
        Generate notes in a conversational style that a presenter
        could read to present the slide to an audience.
        '''

    messages = [{
        'role': 'user',
        'content': [
            { 'type': 'text', 'text': f'{prompt}' },
            { 'type': 'image_url', 'image_url': { 'url': f'{image_url}' }}
        ]
    }]

    client = OpenAI(api_key=openai_api_key)

    response = client.chat.completions.create(
        model='gpt-4o',
        messages=messages
    )

    return response.choices[0].message.content

def encode_image(image_url):
    with open(image_url, 'rb') as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_string

def generate_audio(text, audio_url):
    client = OpenAI(api_key=openai_api_key)

    response = client.audio.speech.create(
        model='tts-1',
        voice='fable',
        input=text
    )

    with open(audio_url, 'wb') as audio_file:
        audio_file.write(response.content)

    return audio_url