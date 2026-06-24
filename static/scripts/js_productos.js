document.addEventListener('DOMContentLoaded', async () => {
    try {
        const response = await fetch('/api/carrito');
        const carritoData = await response.json();
        actualizarCarritoUI(carritoData);
    } catch (err) {
        console.error('Error al cargar el carrito:', err);
        actualizarCarritoUI({});
    }
});

async function agregarAlCarrito(productoId) {
    try {
        const response = await fetch('/api/carrito/agregar', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ id: productoId })
        });
        const data = await response.json();
        if (data.carrito) {
            actualizarCarritoUI(data.carrito);
        }
    } catch (err) {
        console.error('Error al agregar:', err);
    }
}

async function eliminarDelCarrito(productoId) {
    try {
        const response = await fetch('/api/carrito/eliminar', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ id: productoId })
        });
        const data = await response.json();
        if (data.carrito !== undefined) {
            actualizarCarritoUI(data.carrito);
        }
    } catch (err) {
        console.error('Error al eliminar:', err);
    }
}

// ==========================================
// FUNCIÓN DE COMPRA MODIFICADA PARA EL PAGO
// ==========================================
async function comprarCarrito() {
    // 1. Capturar cuál radio button está marcado en la interfaz
    const radioMarcado = document.querySelector('input[name="metodo_pago"]:checked');
    const metodoSeleccionado = radioMarcado ? radioMarcado.value : 'Efectivo';

    try {
        const response = await fetch('/api/carrito/comprar', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ metodo_pago: metodoSeleccionado })
        });
        
        // 2. Leer la respuesta como texto primero para manejar errores
        const responseText = await response.text();
        let data;
        try {
            data = JSON.parse(responseText);
        } catch (parseError) {
            // Si no es JSON, mostrar el texto
            alert('Error: El servidor respondió con un formato inesperado.');
            console.error('Respuesta no JSON:', responseText);
            return;
        }
        
        if (response.ok) {
            alert(`¡Compra procesada con éxito!\nMétodo: ${metodoSeleccionado}\n${data.mensaje || ''}`);
            actualizarCarritoUI({});
        } else {
            alert(data.error || 'Ocurrió un error inesperado al procesar la compra.');
        }
    } catch (err) {
        console.error('Error al comprar:', err);
        alert('Error de conexión con el servidor. Verifica que el servidor esté corriendo.');
    }
}

// ==========================================
// RENDERIZADO OPTIMIZADO CON BOOTSTRAP 5
// ==========================================
function actualizarCarritoUI(carritoData) {
    const container = document.getElementById('carrito-items');
    const vacioMsg = document.getElementById('carrito-vacio');
    const items = Object.values(carritoData);

    if (items.length === 0) {
        container.style.display = 'none';
        vacioMsg.style.display = 'block';
        container.innerHTML = '';
        return;
    }

    vacioMsg.style.display = 'none';
    container.style.display = 'block';

    let total = 0;
    let html = '';

    // Renderizar los productos con diseño Bootstrap de lista limpia
    items.forEach(item => {
        const subtotal = item.precio * item.cantidad;
        total += subtotal;
        html += `
            <div class="d-flex justify-content-between align-items-center bg-light p-2 rounded mb-2 border-start border-warning border-3 shadow-sm">
                <div style="max-width: 70%;">
                    <strong class="d-block small text-dark text-truncate">${item.nombre}</strong>
                    <span class="text-muted small">S/ ${item.precio.toFixed(2)} × ${item.cantidad}</span>
                </div>
                <div class="text-end d-flex align-items-center gap-2">
                    <span class="small fw-bold text-dark">S/ ${subtotal.toFixed(2)}</span>
                    <button class="btn btn-link text-danger p-0 border-0 lh-1" onclick="eliminarDelCarrito(${item.id})" title="Quitar uno">
                        <i class="bi bi-dash-circle-fill fs-5"></i>
                    </button>
                </div>
            </div>
        `;
    });

    // Inyectar el selector visual de Métodos de Pago usando el componente "btn-check"
    html += `
        <div class="border-top pt-3 mb-3">
            <label class="form-label text-dark fw-bold small mb-2">
                <i class="bi bi-credit-card-2-front-fill text-muted me-1"></i> Método de Pago:
            </label>
            <div class="d-flex flex-column gap-2">
                
                <div class="form-check p-0 m-0">
                    <input type="radio" class="btn-check" name="metodo_pago" id="pago-efectivo" value="Efectivo" checked autocomplete="off">
                    <label class="btn btn-outline-secondary w-100 text-start py-2 px-3 d-flex align-items-center gap-2" for="pago-efectivo">
                        <i class="bi bi-cash text-success fs-5"></i> <span>Efectivo</span>
                    </label>
                </div>

                <div class="form-check p-0 m-0">
                    <input type="radio" class="btn-check" name="metodo_pago" id="pago-tarjeta" value="Tarjeta" autocomplete="off">
                    <label class="btn btn-outline-secondary w-100 text-start py-2 px-3 d-flex align-items-center gap-2" for="pago-tarjeta">
                        <i class="bi bi-credit-card text-primary fs-5"></i> <span>Tarjeta Débito / Crédito</span>
                    </label>
                </div>

                <div class="form-check p-0 m-0">
                    <input type="radio" class="btn-check" name="metodo_pago" id="pago-yape" value="Yape (QR)" autocomplete="off">
                    <label class="btn btn-outline-secondary w-100 text-start py-2 px-3 d-flex align-items-center gap-2" for="pago-yape">
                        <i class="bi bi-qr-code-scan text-info fs-5"></i> <span>QR Yape</span>
                    </label>
                </div>

            </div>
        </div>

        <div class="border-top pt-2 mt-3">
            <div class="d-flex justify-content-between fw-bold fs-5 mb-3 text-dark">
                <span>Total General:</span>
                <span class="text-success">S/ ${total.toFixed(2)}</span>
            </div>
            <button id="btn-comprar" class="btn btn-success w-100 fw-bold py-2 shadow-sm d-flex align-items-center justify-content-center gap-2" onclick="comprarCarrito()">
                <i class="bi bi-check-circle-fill"></i> Confirmar compra
            </button>
        </div>
    `;

    container.innerHTML = html;
}