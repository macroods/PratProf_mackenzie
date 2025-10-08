
// --- Dados básicos ---

const lista = document.getElementById("listaRestaurantes");
const modal = document.getElementById("modal");
const modalNome = document.getElementById("modalNome");
const dataReserva = document.getElementById("dataReserva");
const horarioReserva = document.getElementById("horarioReserva");
const btnCancelar = document.getElementById("btnCancelar");
const btnConfirmar = document.getElementById("btnConfirmar");

let restauranteAtual = null;

// Renderiza a lista
function renderRestaurantes() {
  lista.innerHTML = "";
  restaurantes.forEach(r => {
    const card = document.createElement("div");
    card.className = "restaurante-card";
    card.innerHTML = `
      <h3 class="font-semibold text-lg">${r.nome}</h3>
      <div class="flex flex-wrap gap-2 mt-2">
        ${r.horarios.map(h => `<span class="px-2 py-1 border rounded-lg text-sm">${h}</span>`).join("")}
      </div>
      <button class="btn-reservar mt-4" data-id="${r.id}">Reservar</button>
    `;
    lista.appendChild(card);
  });

  document.querySelectorAll(".btn-reservar").forEach(btn => {
    btn.addEventListener("click", () => abrirModal(+btn.dataset.id));
  });
}

// Abre modal
function abrirModal(id) {
  restauranteAtual = restaurantes.find(r => r.id === id);
  modalNome.textContent = restauranteAtual.nome;
  horarioReserva.innerHTML = restauranteAtual.horarios.map(h => `<option value="${h}">${h}</option>`).join("");
  modal.classList.remove("hidden");
}

// Fecha modal
function fecharModal() {
  modal.classList.add("hidden");
}

btnCancelar.addEventListener("click", fecharModal);
modal.addEventListener("click", e => { if (e.target === modal) fecharModal(); });

btnConfirmar.addEventListener("click", () => {
  const data = dataReserva.value;
  const horario = horarioReserva.value;
  if (!data || !horario) {
    alert("Escolha data e horário para confirmar!");
    return;
  }
  alert(`Reserva confirmada em ${restauranteAtual.nome} para ${data} às ${horario}.`);
  fecharModal();
});

renderRestaurantes();