import streamlit as st
from groq import Groq

st.set_page_config(page_title="Mi chat de IA", page_icon="😎")
nombre = ""
st.title("¡Bienvenido! Un gusto verlo.")
nombre = st.text_input("¿Cuál es su nombre?")
if st.button("Saludito") :
    st.write(f"Hola, {nombre}!, Espero que estes bien :)")

MODELO = ['llama3-8b-8192', 'llama3-70b-8192', 'mixtral-8x7b-32768']

#Conectar a la API
def crear_usuario_groq():
    clave_secreta = st.secrets["CLAVE_API"] #Toma la clave
    return Groq(api_key = clave_secreta) #Crear el usuario

def configurar_modelo(cliente, modelo, mensajeEntrente):
    return cliente.chat.completions.create(
        model = modelo,
        messages = [{"role":"user","content": mensajeEntrente}], #Quin manda el mensaje
        stream = True
    )

def inicializar_estado():# --> Historial de mensajes
    # si mansajes no esta en st.session_state: el usuario nunca ingreso un mensaje
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = [] #Memoria de mensajes

def actualizar_historial(rol, contenido, avatar):
     st.session_state.mensajes.append({"role":rol, "content":contenido, "avatar": avatar})

def mostrar_historial():
    for mensaje in st.session_state.mensajes:
        # with crea el apartado del mansaje, hace un bloque agrupando el avatar, el usuario y el mansaje
        with st.chat_message(mensaje["role"], avatar = mensaje["avatar"]) : st.markdown(mensaje["content"])

# Contenedor del chat
def area_chat():
    contenedorDelChat = st.container(height=400, border= True)
    # Agrupamos los mensajes en el area del chta
    with contenedorDelChat: mostrar_historial()

def generar_respuesta(chat_completo):
    respuesta_completa = ""
    for frase in chat_completo:
        if frase.choices[0].delta.content:
            respuesta_completa += frase.choices[0].delta.content
            yield frase.choices[0].delta.content
    return respuesta_completa

# Creando una función -> con diseño de la pagina
def config_web():
    st.title("Mi chat de IA re pro.")
    st.sidebar.title("Configuración.")
    # seleccion2 = st.selectbox
    seleccion1 = st.sidebar.selectbox(
        "Elegi un modelo",
        MODELO,
        index = 0
    )
    return seleccion1

def main():
    #-----------------------------INVOCACIÓN DE FUNCIONES-----------------------------
    modelo = config_web()
    clienteUsuario = crear_usuario_groq()
    inicializar_estado()
    area_chat() #Creamos el sector donde vemos los mensajes
    mensaje = st.chat_input("Hola, ¿Cuánto vale la raíz cuadrada de 2?")
    # Verificar si el mansaje tiene contenido:
    if mensaje:
        actualizar_historial("user", mensaje, "🦄")
        chat_completo = configurar_modelo(clienteUsuario, modelo, mensaje)
        if chat_completo:
            with st.chat_message("assistant"):
                respuesta_completa = st.write_stream(generar_respuesta(chat_completo))
                actualizar_historial("assistant", respuesta_completa, "🤖")
                st.rerun()


        # generar_respuesta(chat_completo)
        # actualizar_historial("assistant", chat_completo, "🤖")
        # st.rerun()


    # st.write(f'El usuario elegio la opcion "{modelo}".')

#Indicamos que nuestra funcion principal es main
# if __name__ == "__name__":
#     main()
main()