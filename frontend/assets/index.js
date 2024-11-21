async function logout(event){
    event.preventDefault();
    try {
        await fetch('/account/logout/', {
            method: 'GET'
        });

        window.location.href = '/page/login';  // Перенаправляем пользователя на страницу логина
        console.log('должен был случится редирект')

    } catch (error) {
        console.error('Ошибка:', error);
    }
}

