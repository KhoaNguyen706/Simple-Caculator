import pygame

pygame.init()
window = pygame.display.set_mode((360, 600))
pygame.display.set_caption('Calculator')

running = True

def draw_pressed_button(pos, radius, color):
    pygame.draw.circle(window, color, pos, radius)

def display_text(text, x, y, color, size):
    font = pygame.font.Font('freesansbold.ttf', size)
    text_surface = font.render(text, True, color)
    window.blit(text_surface, (x, y))

def is_button_clicked(pos, button_pos, radius):
    return (pos[0] - button_pos[0]) ** 2 + (pos[1] - button_pos[1]) ** 2 <= radius ** 2

grey = (128, 128, 128)
yellow = (204, 204, 0)
grey_p = (42, 42, 42)
black = (0, 0, 0)
white = (255, 255, 255)

buttons = [
    ((50, 240), 30, grey, 'AC'),
    ((140, 240), 30, grey, '+/-'),
    ((230, 240), 30, grey, '%'),
    ((310, 240), 30, yellow, '/'),
    ((310, 320), 30, yellow, 'x'),
    ((310, 400), 30, yellow, '-'),
    ((310, 480), 30, yellow, '+'),
    ((310, 560), 30, yellow, '='),
    ((50, 320), 30, grey_p, '7'),
    ((140, 320), 30, grey_p, '8'),
    ((230, 320), 30, grey_p, '9'),
    ((50, 400), 30, grey_p, '4'),
    ((140, 400), 30, grey_p, '5'),
    ((230, 400), 30, grey_p, '6'),
    ((50, 480), 30, grey_p, '1'),
    ((140, 480), 30, grey_p, '2'),
    ((230, 480), 30, grey_p, '3'),
    ((50, 560), 30, grey_p, '0'),
    ((140, 560), 30, grey_p, '00'),
    ((230, 560), 30, grey_p, '.')
]

calu = []

def calculate_expression(expression):
    try:
        # Replace 'x' with '*' for multiplication
        expression = expression.replace('x', '*')
        # Evaluate the expression
        result = eval(expression)
        result=round(result,2)
        return str(result)
    except Exception as e:
        return "Error"

# Main Loop
while running:
    window.fill((0, 0, 0))  # Clear the screen

    for button in buttons:
        pos, radius, color, text = button
        draw_pressed_button(pos, radius, color)
        display_text(text, pos[0] - 10, pos[1] - 10, white if color != grey else black, 32)

    # Display the clicked numbers aligned to the right
    expression = ''.join(calu)
    text_surface = pygame.font.Font('freesansbold.ttf', 100).render(expression, True, white)  # Increased font size
    text_rect = text_surface.get_rect()
    text_rect.topright = (350, 100)
    window.blit(text_surface, text_rect)

    pygame.display.update()  # Update the display once per frame

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            for button in buttons:
                pos, radius, color, text = button
                if is_button_clicked(mouse_pos, pos, radius):
                    print(f'Button {text} clicked')
                    if text in "012345678900":
                        calu.append(text)
                    elif text == "AC":
                        calu.clear()
                    elif text in "+-x/=.":
                        if text == "=":
                            expression = ''.join(calu)
                            result = calculate_expression(expression)
                            calu = list(result)
                        else:
                            calu.append(text)
                    elif text in "+/-":
                        if calu and calu[-1].isdigit():
                            # Find the start of the current number
                            i = len(calu) - 1
                            while i > 0 and calu[i-1].isdigit():
                                i -= 1
                            if i > 0 and calu[i-1] == '-':
                                calu.pop(i-1)
                            else:
                                calu.insert(i, '-')
                    elif text == "%":
                       if calu and calu[-1].isdigit():
                            # Find the start of the current number
                            i = len(calu) - 1
                            while i > 0 and calu[i-1].isdigit():
                                i -= 1
                            # Get the current number
                            current_number = ''.join(calu[i:])
                            # Divide the current number by 100
                            new_number = str(float(current_number) / 100)
                            # Replace the current number with the new number
                            calu = calu[:i] + list(new_number)
                    print(calu)

pygame.quit()
