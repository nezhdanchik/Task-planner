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

async function deleteTask(event){
    event.preventDefault();
    const button = event.target;
    const card = button.closest('.card');
    const taskId = card.dataset.taskId;


    try {
        await fetch(`/task/${taskId}`, {
            method: 'DELETE'
        });
        card.remove();

    } catch (error) {
        console.error('Ошибка:', error);
    }
}

async function changeStatus(event, newStatus){
    event.preventDefault();
    const button = event.target;
    const card = button.closest('.card');
    const taskId = card.dataset.taskId;

    try {
        await fetch(`/task/${taskId}/status`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({status: newStatus})
        });

        if (newStatus === 'completed') {
            await fetch(`/task/${taskId}/end/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
            })
        }

        location.reload();

    } catch (error) {
        console.error('Ошибка:', error);
    }

}