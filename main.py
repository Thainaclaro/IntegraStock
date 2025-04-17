import customtkinter as ctk
from tkinter import messagebox
import requests
import json

ctk.set_appearance_mode('light') 
link = 'https://appestoque-e1795-default-rtdb.firebaseio.com/'

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("IntegraStock")
        self.geometry("300x500")

        self.pages = {}
        for Page in (LogPage, CadPage, EstogPage, PagPage, PagForn, PagGeral):
            page = Page(self)
            self.pages[Page] = page

        self.show_page(LogPage)

    def show_page(self, page_class):
        for page in self.pages.values():
            page.pack_forget()
        self.pages[page_class].pack(fill="both", expand=True)


class LogPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        log_user = ctk.CTkLabel(self, text="LOGIN")
        log_user.pack(pady=20)

        self.log_emp = ctk.CTkEntry(self, placeholder_text='Nome da empresa:')
        self.log_emp.pack(pady=10)

        self.log_cnpj = ctk.CTkEntry(self, placeholder_text='Cnpj da empresa:')
        self.log_cnpj.pack(pady=10)

        self.log_senha = ctk.CTkEntry(self, placeholder_text='Senha da empresa:', show='*')
        self.log_senha.pack(pady=10)

        btn = ctk.CTkButton(self, text='Logar', command=self.validar_login)
        btn.pack(pady=10)

        btn_cad = ctk.CTkButton(self, text='Cadastre-se', command=lambda: master.show_page(CadPage))
        btn_cad.pack()

    def validar_login(self):
        cnpj = self.log_cnpj.get()
        senha = self.log_senha.get()

        if not cnpj or not senha:
            messagebox.showerror("Erro", "Preencha CNPJ e Senha.")
            return

        try:
            response = requests.get(f'{link}/Cadastro.json').json()
            for item in response.values():
                if item['Cnpj'] == cnpj and item['Senha'] == senha:
                    messagebox.showinfo("Sucesso", "Login realizado!")
                    self.master.show_page(EstogPage)
                    return
            messagebox.showerror("Erro", "CNPJ ou senha incorretos.")
        except:
            messagebox.showerror("Erro", "Erro de conexão com o servidor.")


class CadPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        cad_user = ctk.CTkLabel(self, text="CADASTRO")
        cad_user.pack(pady=20)

        self.cad_NomeEmpresa = ctk.CTkEntry(self, placeholder_text='Nome da Empresa:')
        self.cad_NomeEmpresa.pack(pady=20)

        self.cad_cnpj = ctk.CTkEntry(self, placeholder_text='Cnpj da empresa:')
        self.cad_cnpj.pack(pady=10)

        self.cad_senha = ctk.CTkEntry(self, placeholder_text='Digite uma senha:', show='*')
        self.cad_senha.pack(pady=10)

        self.cad_ConfSenha = ctk.CTkEntry(self, placeholder_text='Confirme sua Senha:', show='*')
        self.cad_ConfSenha.pack(pady=10)

        btn_testar = ctk.CTkButton(self, text='Cadastrar', command=self.testar_dados)
        btn_testar.pack(pady=10)

        btn_voltar = ctk.CTkButton(self, text='Sair', command=lambda: master.show_page(LogPage))
        btn_voltar.pack()

    def testar_dados(self):
        nome = self.cad_NomeEmpresa.get()
        cnpj = self.cad_cnpj.get()
        senha = self.cad_senha.get()
        conf_senha = self.cad_ConfSenha.get()

        if not nome or not cnpj or not senha or not conf_senha:
            messagebox.showerror("Erro", "Preencha todos os campos.")
            return

        if senha != conf_senha:
            messagebox.showerror("Erro", "As senhas não coincidem.")
            return

        try:
            verifica = requests.get(f"{link}/Cadastro.json").json()
            for item in verifica.values():
                if item['Cnpj'] == cnpj:
                    messagebox.showerror("Erro", "CNPJ já cadastrado.")
                    return
        except:
            messagebox.showerror("Erro", "Erro ao verificar o banco de dados.")
            return

        dados = {'NomeEmpresa': nome, 'Cnpj': cnpj, 'Senha': senha}
        requests.post(f'{link}/Cadastro.json', data=json.dumps(dados))
        messagebox.showinfo("Sucesso", "Cadastro realizado com sucesso!")
        self.master.show_page(LogPage)


class EstogPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        estog_label = ctk.CTkLabel(self, text="Página de Estoque")
        estog_label.pack(pady=20)

        btn_cadProd = ctk.CTkButton(self, text='Adicionar Produto', command=lambda: master.show_page(PagPage))
        btn_cadProd.pack(pady=10)

        btn_cadforn = ctk.CTkButton(self, text='Adicionar fornecedor', command=lambda: master.show_page(PagForn))
        btn_cadforn.pack(pady=10)

        btn_visao = ctk.CTkButton(self, text='Visão geral', command=lambda: master.show_page(PagGeral))
        btn_visao.pack(pady=10)

        btn_voltar = ctk.CTkButton(self, text='Sair', command=lambda: master.show_page(LogPage))
        btn_voltar.pack()


class PagPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        prop = ctk.CTkLabel(self, text="ADICIONAR PRODUTOS")
        prop.pack(pady=20)

        self.prop_name = ctk.CTkEntry(self, placeholder_text='Digite o Produto:')
        self.prop_name.pack(pady=10)

        self.prop_Atual = ctk.CTkEntry(self, placeholder_text='Estoque Atual:')
        self.prop_Atual.pack(pady=10)

        self.prop_Max = ctk.CTkEntry(self, placeholder_text='Estoque Maximo:')
        self.prop_Max.pack(pady=10)

        self.prop_min = ctk.CTkEntry(self, placeholder_text='Estoque Minimo')
        self.prop_min.pack(pady=10)

        btn_adc = ctk.CTkButton(self, text='Adicionar', command=self.adc_produto)
        btn_adc.pack(pady=10)

        btn_voltar = ctk.CTkButton(self, text='Voltar', command=lambda: master.show_page(EstogPage))
        btn_voltar.pack(pady=10)

    def adc_produto(self):
        dados = {
            'NomeProduto': self.prop_name.get(),
            'QuantAtual': self.prop_Atual.get(),
            'QuantMax': self.prop_Max.get(),
            'QuantMin': self.prop_min.get()
        }
        requesicao = requests.post(f'{link}/Produtos.json', data=json.dumps(dados))
        print(requesicao)
        print(requesicao.text)


class PagForn(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        forn = ctk.CTkLabel(self, text="ADICIONAR FORNECEDOR")
        forn.pack(pady=20)

        self.forn_NomeFornecedor = ctk.CTkEntry(self, placeholder_text='Nome do fornecedor')
        self.forn_NomeFornecedor.pack(pady=20)

        forn_cont = ctk.CTkLabel(self, text="Meio de contatos")
        forn_cont.pack(pady=20)

        self.forn_tel = ctk.CTkEntry(self, placeholder_text='Digite o telefone:')
        self.forn_tel.pack(pady=10)

        self.forn_Email = ctk.CTkEntry(self, placeholder_text='Digite email')
        self.forn_Email.pack(pady=10)

        btn_add = ctk.CTkButton(self, text='Adicionar', command=self.adc_forn)
        btn_add.pack(pady=10)

        btn_voltar = ctk.CTkButton(self, text='Voltar', command=lambda: master.show_page(EstogPage))
        btn_voltar.pack(pady=10)

    def adc_forn(self):
        dados = {
            'NomeFornecedor': self.forn_NomeFornecedor.get(),
            'Telefone': self.forn_tel.get(),
            'Email': self.forn_Email.get()
        }
        requesicao = requests.post(f'{link}/Forncedor.json', data=json.dumps(dados))
        print(requesicao)
        print(requesicao.text)


class PagGeral(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        geral = ctk.CTkLabel(self, text="VISÃO GERAL")
        geral.pack(pady=20)

        btn_refresh = ctk.CTkButton(self, text='Atualizar Dados', command=self.mostrar_dados)
        btn_refresh.pack(pady=10)

        self.textbox = ctk.CTkTextbox(self, width=250, height=300)
        self.textbox.pack(pady=10)

        btn_voltar = ctk.CTkButton(self, text='Voltar', command=lambda: master.show_page(EstogPage))
        btn_voltar.pack(pady=10)

    def mostrar_dados(self):
        self.textbox.delete("1.0", "end")

        try:
            produtos = requests.get(f'{link}/Produtos.json').json()
            fornecedores = requests.get(f'{link}/Forncedor.json').json()

            self.textbox.insert("end", "PRODUTOS:\n")
            for item in produtos.values():
                nome = item['NomeProduto']
                atual = int(item['QuantAtual'])
                minimo = int(item['QuantMin'])
                self.textbox.insert("end", f"{nome} - Atual: {atual}, Mínimo: {minimo}\n")
                if atual < minimo:
                    self.textbox.insert("end", "⚠ REPOSIÇÃO NECESSÁRIA\n")
            
            self.textbox.insert("end", "\nFORNECEDORES:\n")
            for item in fornecedores.values():
                self.textbox.insert("end", f"{item['NomeFornecedor']} - Tel: {item['Telefone']}, Email: {item['Email']}\n")

        except:
            self.textbox.insert("end", "Erro ao carregar dados.")


app = MainApp()
app.mainloop()