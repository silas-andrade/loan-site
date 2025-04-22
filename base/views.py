from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from collections import defaultdict
from .models import Material, Usuario, EmprestimoMaterial, Configuracao
from .forms import MaterialForm, UsuarioCadastroForm, EmprestimoForm


#  login
def loginPage(request):
    if request.method == 'POST':
        matricula = request.POST.get('matricula')
        password = request.POST.get('password')

        if matricula and password:
            user = authenticate(request, username=matricula, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('indexAdm' if user.is_staff else 'emprestimo')
            else:
                messages.error(request, 'Matrícula ou senha inválidos.')
        else:
            messages.error(request, 'Preencha todos os campos.')

        return redirect('login')

    return render(request, 'base/login.html')

#  cadastro
def cadastrar(request):
    if request.method == 'POST':
        form = UsuarioCadastroForm(request.POST)
        if form.is_valid():
            Usuario.objects.create_user(
                nome=form.cleaned_data['nome'],
                matricula=form.cleaned_data['matricula'],
                ano=form.cleaned_data['ano'],
                turma=form.cleaned_data['turma'],
                password=form.cleaned_data['senha']
            )
            messages.success(request, 'Usuário registrado com sucesso!')
            return redirect('emprestimo')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = UsuarioCadastroForm()

    return render(request, 'base/cadastrar.html', {'form': form})




#  material 
def materiais(request):
    if request.method == 'POST':
        form = MaterialForm(request.POST)
        if form.is_valid():
            material = form.save(commit=False)
            material.quantidade_disponivel = material.quantidade_total
            material.save()
            return redirect('material')
    else:
        form = MaterialForm()

    materiais = Material.objects.all()
    return render(request, 'base/material.html', {'form': form, 'materiais': materiais})


#remover material
def remover_material(request, id):
    material = Material.objects.filter(id=id).first()
    if material and request.method == 'POST':
        material.delete()
    return redirect('material')


# lista de usuários 
@login_required
def usuarios_view(request):
    usuarios_por_turma = defaultdict(list)
    usuarios = Usuario.objects.filter(is_superuser=False)

    for usuario in usuarios:
        turma = f"{usuario.ano} {usuario.turma}"
        usuarios_por_turma[turma].append(usuario)

    usuarios_adm = Usuario.objects.filter(is_superuser=True)
    usuarios_adm_info = [
        {'usuario': u, 'email': u.email, 'cargo': u.cargo} for u in usuarios_adm
    ]

    total_usuarios = Usuario.objects.count()

    return render(request, 'base/lista_usuario.html', {
        'usuarios_por_turma': dict(usuarios_por_turma),
        'usuarios_adm_info': usuarios_adm_info,
        'total_usuarios': total_usuarios,
    })


@login_required
def bloquear_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    usuario.bloqueado = not usuario.bloqueado
    usuario.save()
    return redirect('lista_usuario')



# configurações do site
def configuracoes(request):
    configuracao, _ = Configuracao.objects.get_or_create(id=1)

    if request.method == 'POST':
        configuracao.aceitar_automaticamente = 'toggle_auto_aceite' in request.POST
        configuracao.bloquear_emprestimos = 'toggle_bloqueio' in request.POST
        configuracao.save()

        return redirect('configuracoes')

    return render(request, 'base/configuracoes.html', {
        'aceitar_automaticamente': configuracao.aceitar_automaticamente,
        'bloquear_emprestimos': configuracao.bloquear_emprestimos,
    })




#verifique daqui 



#  Solicitar empréstimo
@login_required
def solicitar_emprestimo(request):
    usuario = request.user
    config = Configuracao.objects.first()

    if usuario.bloqueado:
        messages.error(request, 'Você está bloqueado e não pode solicitar empréstimos.')
        return redirect('emprestimo')

    if config and config.bloquear_emprestimos:
        messages.error(request, 'Os empréstimos estão temporariamente desativados pelo administrador.')
        return redirect('emprestimo')

    if request.method == 'POST':
        form = EmprestimoForm(request.POST)
        if form.is_valid():
            emprestimo = form.save(commit=False)
            emprestimo.usuario = usuario
            emprestimo.devolvido = config.aceitar_automaticamente if config else False
            emprestimo.save()

            emprestimo.material.quantidade_disponivel -= emprestimo.quantidade
            emprestimo.material.save()

            if emprestimo.devolvido:
                messages.success(request, f"Empréstimo aceito automaticamente! Devolução prevista: {emprestimo.data_prevista_devolucao.strftime('%d/%m/%Y')}")
            else:
                messages.success(request, "Solicitação de empréstimo enviada com sucesso. Aguarde aprovação do administrador.")

            return redirect('emprestimo')
        else:
            messages.error(request, 'Erro ao enviar o formulário. Verifique os campos.')
    else:
        form = EmprestimoForm()

    return render(request, 'base/emprestimo.html', {'form': form})


#  página do adm 
from django.utils import timezone




@login_required
def indexAdm(request):
    configuracao = Configuracao.objects.first()
    aceitar_automaticamente = configuracao.aceitar_automaticamente if configuracao else False

    pedidos_pendentes = EmprestimoMaterial.objects.filter(status=EmprestimoMaterial.PENDENTE)
    
   
    if aceitar_automaticamente:
        for pedido in pedidos_pendentes:
            pedido.status = EmprestimoMaterial.ACEITO
            pedido.save()

    pedidos_aceitos = EmprestimoMaterial.objects.filter(
        status=EmprestimoMaterial.ACEITO
    ).order_by('data_prevista_devolucao')

    pedidos_devolvidos = EmprestimoMaterial.objects.filter(status=EmprestimoMaterial.DEVOLVIDO)

    for pedido in pedidos_aceitos:
        pedido.dias_restantes = (pedido.data_prevista_devolucao - timezone.now().date()).days
    
    return render(request, 'base/indexAdm.html', {
        'pedidos_pendentes': pedidos_pendentes,
        'pedidos_aceitos': pedidos_aceitos,
        'pedidos_devolvidos': pedidos_devolvidos,
    })








#  pedidos


@login_required
def aceitar_pedido(request, pedido_id):
    pedido = get_object_or_404(EmprestimoMaterial, id=pedido_id)
    
    # Altera o status pra aceito
    pedido.status = EmprestimoMaterial.ACEITO
    pedido.save()

    return redirect('indexAdm')



@login_required
def recusar_pedido(request, pedido_id):
    pedido = get_object_or_404(EmprestimoMaterial, id=pedido_id)

    pedido.delete()

    return redirect('indexAdm')

@login_required
def recusar_devolucao(request, pedido_id):
    pedido = get_object_or_404(EmprestimoMaterial, id=pedido_id)

    # volta para aceito
    if pedido.status == EmprestimoMaterial.DEVOLVIDO:
        pedido.status = EmprestimoMaterial.ACEITO
        pedido.save()

    return redirect('indexAdm')


@login_required
def confirmar_devolucao(request, pedido_id):
    pedido = get_object_or_404(EmprestimoMaterial, id=pedido_id)
    
    # Alterar o status 
    if pedido.status == EmprestimoMaterial.ACEITO:
        pedido.status = EmprestimoMaterial.DEVOLVIDO
        pedido.save()

    return redirect('indexAdm')
