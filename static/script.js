// script para renderizar e filtrar restaurantes

const lista = document.getElementById("listaRestaurantes");
const searchInput = document.getElementById('searchInput');

// usa a variável injetada pelo template
const restaurantes = window.restaurantes || [];

// renderiza todos os restaurantes
function renderRestaurantes() {
  if (!lista) return;
  lista.innerHTML = "";

  restaurantes.forEach(r => {
    const card = document.createElement("div");
    card.className = "restaurante-card card";
    const nome = r.nome || r['nome'] || 'Sem nome';

    // horários reservados (array de strings)
    const reservados = (r.horarios_reservados || r['horarios_reservados'] || []).map(s => String(s).trim());

    // montar horários: suporta campo horario_disponivel (string) ou r.horarios (array)
    let horariosHtml = "";
    if (r.horario_disponivel && typeof r.horario_disponivel === "string") {
      horariosHtml = r.horario_disponivel.split(',').map(h => {
        const hh = h.trim();
        if (reservados.includes(hh)) {
          // horário indisponível
          return `<span class="horario-item horario-indisponivel">${hh}</span>`;
        } else {
          // horário disponível
          return `<button class="horario-item btn" data-h="${hh}" data-id="${r.id || r['id'] || ''}">${hh}</button>`;
        }
      }).join('');
    } else if (Array.isArray(r.horarios)) {
      horariosHtml = r.horarios.map(h => {
        const hh = String(h).trim();
        if (reservados.includes(hh)) {
          return `<span class="horario-item horario-indisponivel">${hh}</span>`;
        } else {
          return `<button class="horario-item btn" data-h="${hh}" data-id="${r.id || r['id'] || ''}">${hh}</button>`;
        }
      }).join('');
    }

    card.innerHTML = `
      <h3>${nome}</h3>
      <div class="card-horarios">${horariosHtml}</div>
    `;
    lista.appendChild(card);
  });

  // listeners para horários disponíveis: navega para /reserva/<id>?horario=...
  document.querySelectorAll(".horario-item.btn").forEach(el => {
    el.addEventListener("click", () => {
      const id = el.dataset.id;
      const h = el.dataset.h;
      if (!id || !h) return;
      const url = `/reserva/${id}?horario=${encodeURIComponent(h)}`;
      location.href = url;
    });
  });
}

// filtro: só aplica quando há texto
function setupFiltro() {
  if (!searchInput) return;
  searchInput.addEventListener('input', function() {
    const q = this.value.trim().toLowerCase();
    const cards = document.querySelectorAll('#listaRestaurantes .restaurante-card');
    if (!q) {
      cards.forEach(c => c.style.display = '');
      return;
    }
    cards.forEach(card => {
      const nome = (card.querySelector('h3')?.textContent || '').toLowerCase();
      card.style.display = nome.includes(q) ? '' : 'none';
    });
  });
}

// inicializa
renderRestaurantes();
setupFiltro();