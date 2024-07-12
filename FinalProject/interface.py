import pygame
import time
import better_speech_bot
from openai import OpenAI

client = OpenAI(
    api_key = "sk-proj-lEyW1PTgYBP9bQMeYikkT3BlbkFJQAXez34xx1DY4nYOep0P"
)
start = 0
scrolling = False
recorded = False
talking = False
pygame.init()
pygame.font.init()
background = pygame.image.load("mountainbackground.jpg")
background_rect = background.get_rect()
background_rect.topleft = (0, 0)
robot_idle = pygame.image.load("robot_idle.png")
robot_talking = [pygame.image.load("robot_talking_0.png"),
                pygame.image.load("robot_talking_1.png"),
                pygame.image.load("robot_talking_2.png"),
                pygame.image.load("robot_talking_3.png")]
robot_idle = pygame.transform.scale(robot_idle, (500, 500))
for x in range(len(robot_talking)):
    robot_talking[x] = pygame.transform.scale(robot_talking[x], (500, 500))
frame = 0
robot_rect = robot_idle.get_rect()
font = pygame.font.SysFont("arial", 50)
chat_font = pygame.font.SysFont("arial", 20)
pygame.display.init()
screen_width = pygame.display.get_desktop_sizes()[0][0]
screen_height = pygame.display.get_desktop_sizes()[0][1]
robot_rect.topleft = (screen_width - 450, screen_height / 5)
user_messages = []
ai_messages = []
end = len(user_messages)
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
start_time = pygame.time.get_ticks()
curr_time = pygame.time.get_ticks()
chat_background = pygame.Rect((screen_width / 4) + 15, screen_height / 10, screen_width / 2, screen_height - 100)
exit_button = pygame.Rect(screen_width - 50, 0, 50, 50)
exit_iconPos = [(screen_width - 40, 10), (screen_width - 10, 40), (screen_width - 10, 10), (screen_width - 40, 40)]
pos = screen_height / 9
user_backgrounds = []
ai_backgrounds = []
for a in range(0, 200):
    user_backgrounds.append(pygame.Rect(screen_width / 4 + 20, pos, 350, 55))
    pos += 50
pos = screen_height / 9
for b in range(0, 200):
    ai_backgrounds.append(pygame.Rect(screen_width / 2 + 20, pos, 350, 55))
    pos += 50
running = True

while running:
    chat_position = screen_height / 9
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and exit_button.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(pygame.display.get_surface(), "red", exit_button)
            pygame.display.flip()
            time.sleep(0.1)
            running = False
        if event.type == pygame.MOUSEWHEEL:
            if event.y == 1 and start != 0:
                start -= 1
                scrolling = True
                print("scrolling")
            elif event.y == -1:
                start += 1
        if event.type == pygame.KEYDOWN:
            if pygame.key.get_pressed()[pygame.key.key_code("r")] and not better_speech_bot.recorder.recording:
                better_speech_bot.recorder.start(better_speech_bot.r)
                scrolling = False
                recorded = True
        if event.type == pygame.KEYUP:
            if not pygame.key.get_pressed()[pygame.key.key_code("r")] and recorded:
                recorded = False
                better_speech_bot.recorder.stop(better_speech_bot.r)
                audio_file = open("mic.wav", "rb")
                transcript = client.audio.translations.create(
                    model = "whisper-1",
                    file = audio_file
                )
                system_data = [
                    {
                        "role": "system",
                        "content": "You are an assistant who answers any prompts given to the best of your abilities. Also be funny, unless asked a question about money"

                    },
                    {
                        "role": "user",
                        "content": transcript.text
                    }
                ]
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=system_data
                )
                assistant_response = response.choices[0].message.content
                system_data.append(
                    {
                        "role": "assistant",
                        "content": assistant_response
                    }
                )
                user_messages.append(transcript.text)
                ai_messages.append(assistant_response)
                talking = True

    screen.fill("white")
    screen.blit(background, background_rect)
    pygame.draw.rect(pygame.display.get_surface(), "black", exit_button)
    pygame.draw.line(pygame.display.get_surface(), "white", exit_iconPos[0], exit_iconPos[1], 4)
    pygame.draw.line(pygame.display.get_surface(), "white", exit_iconPos[2], exit_iconPos[3], 4)
    title_box = font.render("Speech-To-Bot", False, (0, 0, 0))
    screen.blit(title_box, ((screen_width / 2) - 160, 0))
    if talking:
        curr_time = pygame.time.get_ticks()
        if frame >= len(robot_talking):
            frame = 0
        image = robot_talking[int(frame)]
        screen.blit(image, robot_rect)
        frame += 0.2
    else:
        screen.blit(robot_idle, robot_rect)
        start_time = pygame.time.get_ticks()
    if curr_time > start_time + 3000:
        talking = False
    if start + 15 <= len(user_messages) and scrolling:
        end = start + 15
    else:
        end = len(user_messages)
    for i in range(start, end):
        n = 35
        split_message = [user_messages[i][z: z + n] for z in range(0, len(user_messages[i]), n)]
        for x in range(len(split_message)):
            print("USER MESSAGES: " + str(int(chat_position / 50)))
            pygame.draw.rect(pygame.display.get_surface(), "blue", user_backgrounds[int(chat_position / 50) - 1], 0, 3)
            user_box = chat_font.render(split_message[x], False, (0, 0, 0))
            screen.blit(user_box, (screen_width / 4 + 25, chat_position))
            chat_position += 50
        split_message = [ai_messages[i][y: y + n] for y in range(0, len(ai_messages[i]), n)]
        for w in range(len(split_message)):
            print("AI MESSAGES: " + str(int(chat_position / 50)))
            pygame.draw.rect(pygame.display.get_surface(), "red", ai_backgrounds[int(chat_position / 50) - 1], 0, 3)
            ai_box = chat_font.render(split_message[w], False, (0, 0, 0))
            screen.blit(ai_box, (screen_width / 2 + 25, chat_position))
            chat_position += 50
        if chat_position > chat_background.y + chat_background.height and not scrolling:
            start += 1
    pygame.display.flip()
    clock.tick(60)
pygame.quit()