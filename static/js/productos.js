document.getElementById('agregar-producto-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const formData = new FormData(this);
    const data = {
        name: formData.get('name'),
        precio: formData.get('precio'),
        localidad: formData.get('localidad')
    };

    fetch('/guardar_producto/', {
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
            document.getElementById('agregar-producto-form').reset();
            // Actualizar la tabla de productos recientes
            actualizarProductosRecientes();
        }
    })
    .catch(error => console.error('Error:', error));
});

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

function actualizarProductosRecientes() {
    fetch('/productos_recientes/')
    .then(response => response.json())
    .then(data => {
        const tbody = document.querySelector('#productos-recientes tbody');
        tbody.innerHTML = '';
        data.productos.forEach(producto => {
            const tr = document.createElement('tr');
            tr.id = `producto-${producto.id}`;
            tr.innerHTML = `
                <td>${producto.name}</td>
                <td>${producto.precio}</td>
                <td>${producto.localidad.name}</td>
                <td>${producto.fecha_inicio}</td>
                <td>${producto.fecha_fin}</td>
                <td><button onclick="eliminarProducto(${producto.id})">Eliminar</button></td>
            `;
            tbody.appendChild(tr);
        });
    })
    .catch(error => console.error('Error:', error));
}

function eliminarProducto(productoId) {
    fetch(`/eliminar_producto/${productoId}/`, {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.getElementById(`producto-${productoId}`).remove();
        } else {
            alert(data.error);
        }
    })
    .catch(error => console.error('Error:', error));
}