async function enterFunction(event) {
    event.preventDefault();  // Предотвращаем стандартное действие формы
    // Получаем форму и собираем данные из неё
    const form = document.getElementById('login-form');
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());

    try {
        const response = await fetch('/account/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        // Проверяем успешность ответа
        if (!response.ok) {
            // Получаем данные об ошибке
            const errorData = await response.json();
            alert('Неправильное имя или пароль');  // Отображаем ошибки
            return;  // Прерываем выполнение функции
        }

        const result = await response.json();
        console.log(result)

        window.location.href = '/page/main';  // Перенаправляем пользователя на страницу логина
        console.log('должен был случится редирект')

    } catch (error) {
        console.error('Ошибка:', error);
        alert('Произошла ошибка при входе. Пожалуйста, попробуйте снова.');
    }
}

