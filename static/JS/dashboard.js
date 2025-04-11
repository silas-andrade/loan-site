let emprestimos = [];

function showSection(sectionId) {
  document.querySelectorAll('.page-section').forEach(sec => sec.style.display = 'none');
  document.getElementById(sectionId).style.display = 'block';
}

function solicitarItem() {
  const item = document.getElementById('itemSelecionado').value;
  const tempo = parseInt(document.getElementById('tempoUso').value);
  const agora = new Date();
  const entrega = new Date(agora.getTime() + tempo * 60 * 60 * 1000);

  if (localStorage.getItem('penalizado') === 'true') {
    alert("Você está penalizado e não pode pegar itens até passar o período.");
    return;
  }

  emprestimos.push({ item, entrega });
  localStorage.setItem('emprestimos', JSON.stringify(emprestimos));

  mostrarEmprestimos();
  alert('Item solicitado com sucesso!');
}

function mostrarEmprestimos() {
  const lista = document.getElementById('listaEmprestimos');
  lista.innerHTML = "<h3>Seus Empréstimos Atuais:</h3>";

  const agora = new Date();
  emprestimos = JSON.parse(localStorage.getItem('emprestimos')) || [];

  emprestimos.forEach((e, i) => {
    const prazo = new Date(e.entrega);
    const atrasado = agora > prazo;
    if (atrasado) {
      localStorage.setItem('penalizado', 'true');
    }
    lista.innerHTML += `<p>${e.item.replace("_", " ")} - Devolver até: ${prazo.toLocaleString()} ${atrasado ? "<strong style='color:red'>(Atrasado)</strong>" : ""}</p>`;
  });
}

function enviarMensagem() {
  const email = document.getElementById('destinatario').value;
  const msg = document.getElementById('mensagem').value;
  if (!email || !msg) {
    alert("Preencha todos os campos.");
    return;
  }

  alert(`Mensagem enviada para ${email}!`);
  document.getElementById('destinatario').value = '';
  document.getElementById('mensagem').value = '';
}

function logout() {
  window.location.href = "index.html";
}

mostrarEmprestimos();
