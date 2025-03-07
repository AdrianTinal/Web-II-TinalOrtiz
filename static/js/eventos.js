document.getElementById('agregar-evento-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const formData = new FormData(this);
    const data = {
        name: formData.get('name'),
        localidad: formData.get('localidad'),
        descripcion: formData.get('descripcion'),
        photo: formData.get('photo'),
        fecha_inicio: formData.get('fecha_inicio'),
        fecha_fin: formData.get('fecha_fin')
    };

    fetch('/guardar/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        const mensajeDiv = document.getElementById('mensaje');
        if (data.error) {
            mensajeDiv.innerHTML = `<p style="color: red;">${data.error}</p>`;
        } else {
            mensajeDiv.innerHTML = `<p style="color: green;">${data.success}</p>`;
            document.getElementById('agregar-evento-form').reset();
            // Actualizar la tabla de eventos recientes
            actualizarEventosRecientes();
        }
    })
    .catch(error => console.error('Error:', error));
});

function eliminarEvento(eventoId) {
    fetch(`/eliminar/${eventoId}/`, {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.getElementById(`evento-${eventoId}`).remove();
        } else {
            alert(data.error);
        }
    })
    .catch(error => console.error('Error:', error));
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function actualizarEventosRecientes() {
    fetch('/eventos_recientes/')
    .then(response => response.json())
    .then(data => {
        const tbody = document.querySelector('#eventos-recientes tbody');
        tbody.innerHTML = '';
        data.eventos.forEach(evento => {
            const tr = document.createElement('tr');
            tr.id = `evento-${evento.id}`;
            tr.innerHTML = `
                <td>${evento.name}</td>
                <td>${evento.fecha_inicio}</td>
                <td>${evento.fecha_fin}</td>
                <td>${evento.localidad.name}</td>
                <td><button onclick="eliminarEvento(${evento.id})">Eliminar</button></td>
            `;
            tbody.appendChild(tr);
        });
    })
    .catch(error => console.error('Error:', error));
}