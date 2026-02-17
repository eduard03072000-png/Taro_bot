from modules.matrix_chart import calculate_matrix, generate_matrix_image

data = calculate_matrix('07.10.1952')
print('Расчет для 07.10.1952:')
for k, v in data.items():
    if k != 'date':
        print(f'  {k} = {v}')

img_bytes = generate_matrix_image('07.10.1952', 'Тест')
with open('test_matrix.png', 'wb') as f:
    f.write(img_bytes)
print(f'OK: {len(img_bytes)} bytes -> test_matrix.png')
