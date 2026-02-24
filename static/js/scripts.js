/**
 * Lógica del Frontend para la Agenda Telefónica
 */

let allContacts = [];

// Escuchar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    fetchContacts();
    
    // Configurar el envío del formulario
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', (e) => {
            e.preventDefault();
            saveContact();
        });
    }
});

/**
 * Obtiene la lista de contactos desde el servidor
 */
async function fetchContacts() {
    try {
        const res = await fetch('/api/contacts');
        allContacts = await res.json();
        renderContacts(allContacts);
    } catch (err) {
        console.error("Error al obtener contactos:", err);
    }
}

/**
 * Dibuja los contactos en la tabla HTML
 */
function renderContacts(contacts) {
    const table = document.getElementById('contactsTable');
    const empty = document.getElementById('emptyState');
    
    if (!table) return;
    
    table.innerHTML = '';
    
    if (contacts.length === 0) {
        empty.classList.remove('hidden');
        return;
    }
    
    empty.classList.add('hidden');

    contacts.forEach(c => {
        const row = document.createElement('tr');
        row.className = "hover:bg-gray-50 transition-colors";
        row.innerHTML = `
            <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex items-center">
                    <div class="h-10 w-10 flex-shrink-0 bg-indigo-100 text-indigo-700 rounded-full flex items-center justify-center font-bold">
                        ${c.name.charAt(0).toUpperCase()}
                    </div>
                    <div class="ml-4">
                        <div class="text-sm font-medium text-gray-900">${c.name}</div>
                        <div class="text-sm text-gray-500">${c.phone}</div>
                    </div>
                </div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                ${c.email || 'N/A'}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                <button onclick="editContact(${c.id})" class="text-indigo-600 hover:text-indigo-900 mr-4">
                    <i class="fas fa-edit"></i>
                </button>
                <button onclick="deleteContact(${c.id})" class="text-red-600 hover:text-red-900">
                    <i class="fas fa-trash"></i>
                </button>
            </td>
        `;
        table.appendChild(row);
    });
}

/**
 * Filtra contactos en tiempo real
 */
async function searchContacts() {
    const term = document.getElementById('searchInput').value;
    try {
        const res = await fetch(`/api/contacts?q=${encodeURIComponent(term)}`);
        const filtered = await res.json();
        renderContacts(filtered);
    } catch (err) {
        console.error("Error en la búsqueda:", err);
    }
}

/**
 * Crea o Actualiza un contacto
 */
async function saveContact() {
    const id = document.getElementById('contactId').value;
    const data = {
        name: document.getElementById('name').value,
        phone: document.getElementById('phone').value,
        email: document.getElementById('email').value
    };

    const method = id ? 'PUT' : 'POST';
    const url = id ? `/api/contacts/${id}` : '/api/contacts';

    try {
        const res = await fetch(url, {
            method: method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        if (res.ok) {
            closeModal();
            fetchContacts();
        } else {
            const errData = await res.json();
            alert("Error: " + errData.error);
        }
    } catch (err) {
        console.error("Error al guardar:", err);
    }
}

/**
 * Elimina un contacto
 */
async function deleteContact(id) {
    if (!confirm('¿Estás seguro de eliminar este contacto?')) return;
    
    try {
        const res = await fetch(`/api/contacts/${id}`, { method: 'DELETE' });
        if (res.ok) fetchContacts();
    } catch (err) {
        console.error("Error al eliminar:", err);
    }
}

/**
 * Prepara el modal para edición
 */
function editContact(id) {
    const contact = allContacts.find(c => c.id === id);
    if (!contact) return;

    document.getElementById('modalTitle').innerText = 'Editar Contacto';
    document.getElementById('contactId').value = contact.id;
    document.getElementById('name').value = contact.name;
    document.getElementById('phone').value = contact.phone;
    document.getElementById('email').value = contact.email || '';
    
    document.getElementById('modal').classList.remove('hidden');
}

/**
 * Utilidades del Modal
 */
function openModal() {
    document.getElementById('modalTitle').innerText = 'Nuevo Contacto';
    document.getElementById('contactId').value = '';
    document.getElementById('contactForm').reset();
    document.getElementById('modal').classList.remove('hidden');
}

function closeModal() {
    document.getElementById('modal').classList.add('hidden');
}