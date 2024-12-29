import os
from pydub import AudioSegment
import gradio as gr
import subprocess
from PIL import Image
import cv2
import sys
import time
from genavaimg import *
from genavatts import *
from hedavatar import *
from registro import *
from hedlogin import *
import shutil
import signal
import sys
import re
import logging


# Configurar el log para registrar errores
logging.basicConfig(filename="app_errors.log", level=logging.ERROR)

# Suprimir errores visibles en la consola (opcional)
sys.stderr = open(os.devnull, 'w')

# Decorador para manejar errores de forma segura
def safe_execution(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"Error en {func.__name__}: {e}")
            return "Ha ocurrido un error. Por favor, revisa tus entradas y vuelve a intentar."
    return wrapper

# Definir el manejador para la interrupción por teclado
def handle_interrupt(signal, frame):
    print("Gradio detenido manualmente. Ruta protegida.")
    sys.exit(0)

# Registrar el manejador para la señal SIGINT
signal.signal(signal.SIGINT, handle_interrupt)

# Función para cargar un video específico
def load_specific_video():
    specific_video_path = "/tmp/videos/0001.mp4"

    if os.path.exists(specific_video_path):
        #print(f"Cargando video específico: {specific_video_path}")
        return [specific_video_path], "Video cargado con éxito."
    else:
        #print(f"Video no encontrado: {specific_video_path}")
        return [], "El video específico no existe."

# Función para escanear videos en la carpeta y devolver una lista de rutas de videos
def scan_videos():
    video_folder = "/tmp/videos"  # Ruta de la carpeta de videos

    # Crear carpeta si no existe
    if not os.path.exists(video_folder):
        os.makedirs(video_folder)

    # Listar solo archivos de video mp4
    videos = [os.path.join(video_folder, f) for f in os.listdir(video_folder) if f.endswith(".mp4")]

    # Ordenar los videos alfanuméricamente
    videos = sorted(videos, key=lambda x: os.path.basename(x).lower())

    # Diagnóstico: Imprimir las rutas encontradas
    print("Videos encontrados (ordenados):")
    print(videos)

    if not videos:
        return [], "No videos encontrados en la carpeta."
    return videos, f"Se encontraron {len(videos)} videos."

# Función para mostrar videos dinámicamente en la interfaz
def handle_video_output_tts():
    videos, message = scan_videos3()

    # Crear una lista de rutas válidas para los componentes `gr.Video`
    video_urls = [video_path for video_path in videos]

    # Verificación en consola
    print("Rutas de videos válidas para mostrar:")
    print(video_urls)

    # Retornar las rutas válidas para renderizarlas en la interfaz
    return video_urls, message
    
# Función para escanear videos en la carpeta y devolver una lista de rutas de videos
def scan_videos3():
    video_folder = "/tmp/videos_tts"  # Ruta de la carpeta de videos

    # Crear carpeta si no existe
    if not os.path.exists(video_folder):
        os.makedirs(video_folder)

    # Listar solo archivos de video mp4
    videos = [os.path.join(video_folder, f) for f in os.listdir(video_folder) if f.endswith(".mp4")]

    # Ordenar los videos alfanuméricamente
    videos = sorted(videos, key=lambda x: os.path.basename(x).lower())

    # Diagnóstico: Imprimir las rutas encontradas
    print("Videos encontrados (ordenados):")
    print(videos)

    if not videos:
        return [], "No videos encontrados en la carpeta."
    return videos, f"Se encontraron {len(videos)} videos."

# Función para mostrar videos dinámicamente en la interfaz
def handle_video_output():
    videos, message = scan_videos()

    # Crear una lista de rutas válidas para los componentes `gr.Video`
    video_urls = [video_path for video_path in videos]

    # Verificación en consola
    print("Rutas de videos válidas para mostrar:")
    print(video_urls)

    # Retornar las rutas válidas para renderizarlas en la interfaz
    return video_urls, message


def run_generate_img_audio_video(prompt, aspect_ratio, seed_input, seed, continue_fragment, process_multiple):
    Aaccess = os.environ.get("ACCESS_TOKEN_HEDRA")

    if Aaccess:
        # Crear la carpeta 'videos' si no existe
        if not os.path.exists('/tmp/videos'):
            os.makedirs('/tmp/videos')

        # Ejemplo de uso
        folder_path = "/tmp/audios/"
        image_path = "/tmp/avatar_img.jpg"
        ruta_videos = "/tmp/videos/"
        #continue_fragment = False
        
        try:
            process_audio_files(folder_path, image_path, ruta_videos, aspect_ratio, prompt, seed_input, seed, continue_fragment, process_multiple)
        except Exception as e:
            raise RuntimeError(f"Error process_audio_files gradio")

    else:
        proceso_completo()
        Aaccess = os.environ.get("ACCESS_TOKEN_HEDRA")
        if Aaccess:
            run_generate_img_audio_video(prompt, aspect_ratio, seed_input, seed, continue_fragment, process_multiple)

    #directory_video = os.environ.get("VIDEO_PATH_HEDRA")


    videos, message = scan_videos()

    # Crear una lista de rutas válidas para los componentes `gr.Video`
    video_urls = [video_path for video_path in videos]

    # Verificación en consola
    print("Rutas de videos válidas para mostrar:")
    print(video_urls)

    # Retornar las rutas válidas para renderizarlas en la interfaz
    return video_urls, message

    # Devuelve la ruta del video y un mensaje
    #return directory_video, "Video creado con éxito"


def join_videos_and_clean(video_folder, output_file):
    try:
        # Verificar si la carpeta existe
        if not os.path.exists(video_folder):
            return "Error: La carpeta no existe.", None

        # Función para dividir texto en partes alfanuméricas y numéricas
        def natural_sort_key(text):
            return [
                int(part) if part.isdigit() else part.lower()
                for part in re.split(r'(\d+)', text)
            ]

        # Obtener y ordenar archivos MP4 con orden natural
        video_files = sorted(
            [f for f in os.listdir(video_folder) if f.endswith(".mp4")],
            key=natural_sort_key
        )

        if not video_files:
            return "Error: No se encontraron archivos MP4 en la carpeta.", None

        # Crear archivo de lista para FFmpeg
        list_file_path = os.path.join(video_folder, "file_list.txt")
        with open(list_file_path, "w") as list_file:
            for video in video_files:
                list_file.write(f"file '{os.path.join(video_folder, video)}'\n")

        # Ejecutar FFmpeg para unir los videos
        command = [
            "ffmpeg",
            "-f", "concat",
            "-safe", "0",
            "-i", list_file_path,
            "-c", "copy",
            output_file
        ]
        subprocess.run(command, check=True)

        # Eliminar archivo de lista temporal
        os.remove(list_file_path)

        # Eliminar los archivos MP4 de la carpeta después de la unión
        for video in video_files:
            os.remove(os.path.join(video_folder, video))

        return "Videos unidos y archivos eliminados exitosamente.", output_file
    except subprocess.CalledProcessError as e:
        return f"Error al unir los videos con FFmpeg: {str(e)}", None
    except Exception as e:
        return f"Error inesperado: {str(e)}", None


# Función conectada al botón Save
def run_save_and_display():

    video_folder = "/tmp/videos"
    output_file = "/tmp/final_video.mp4"  # Archivo final fuera de la carpeta
    message, output_path = join_videos_and_clean(video_folder, output_file)

    if os.path.exists(output_file):
        print(f"Cargando video específico: {output_file}")
        return [output_file], "Video cargado con éxito."
    else:
        print(f"Video no encontrado: {output_file}")
        return [], "El video específico no existe."



# Función para mostrar o ocultar el segundo cuadro de imagen
def activar_end_frame(activar):
    return gr.update(visible=activar)


def run_generate_tts_video(prompt_txt, text, aspect_ratio, selected_tts, use_manual_seed, seed):
    Aaccess = os.environ.get("ACCESS_TOKEN_HEDRA")

    if Aaccess:
        os.makedirs('/tmp/videos_tts', exist_ok=True)

        selected_voice_orignen_id = obtener_id(selected_tts)
        #prompt_txt = ""

        procesar_avatar_request(
            selected_voice_orignen_id,
            use_manual_seed,
            seed,
            aspect_ratio,
            prompt_txt,
            text
        )

    else:
        proceso_completo()
        Aaccess = os.environ.get("ACCESS_TOKEN_HEDRA")
        if Aaccess:
            run_generate_tts_video(prompt_txt, text, aspect_ratio, selected_tts, use_manual_seed, seed)





    #directory_video = os.environ.get("VIDEO_PATH_HEDRA")

    videos, message = scan_videos3()

    # Crear una lista de rutas válidas para los componentes `gr.Video`
    video_urls = [video_path for video_path in videos]

    # Verificación en consola
    print("Rutas de videos válidas para mostrar:")
    print(video_urls)

    # Retornar las rutas válidas para renderizarlas en la interfaz
    return video_urls, message


def run_generate_avatar(prompt_txt, aspect_ratio, negative_prompt_txt, use_manual_seed, seed_number, negative_prompt):

    # Llamar a la función principal
    ejecutar_todo(aspect_ratio, prompt_txt, negative_prompt_txt, use_manual_seed, seed_number, negative_prompt)

    # Devuelve la ruta del video y un mensaje
    return '/tmp/avatar_img.jpg', "Avatar creado con éxito"

# Función para procesar y guardar la imagen automáticamente en formato JPG
def process_and_save_image1(image):

    jpg_path = "/tmp/avatar_img.jpg"

    try:
        if image.format != "JPEG":
            image = image.convert("RGB")
        image.save(jpg_path, "JPEG", quality=100)
        if os.path.exists(jpg_path):
            print(f"Imagen guardada correctamente")

            # Obtener las dimensiones de la imagen
            width, height = image.size

            os.environ["WIDTH_IMG1"] = str(width)
            os.environ["HEIGHT_IMG1"] = str(height)
            os.environ["IMG1"] = jpg_path
            print(jpg_path)

            print(f"Coordenadas guardadas correctamente")

        return None
    except Exception as e:
        print(f"Error al procesar la imagen: {str(e)}")
        return None

# Mapeo de nombres visibles a IDs
nombre_a_id = {
    "Commercial Lady (gender: female)": "c2ac25f9-ecc4-4f56-9095-651354df60c0",
    "Laura (gender: female)": "FGY2WhTYpPnrIDTdsKH5",
    "George (gender: male)": "JBFqnCBsd6RMkjVDRZzb",
    "Emily (gender: female)": "LcfcDJNUP1GQjkzn1xUU",
    "Charlotte (gender: female)": "XB0fDUnXU5powFXDhCwa",
    "Alice (gender: female)": "Xb7hH8MSUJpSbSDYk0k2",
    "Matilda (gender: female)": "XrExE9yKIg1WjnnlVkGX",
    "Will (gender: male)": "bIHbv24MWmeRgasZH58o",
    "Brian (gender: male)": "nPczCjzI2devNBz1zQrb",
    "Lily (gender: female)": "pFZP5JQG7iQjIQuC4Bku",
    "Todd - Universal Crossover (gender: male)": "AQ6yxtsTonfHLHY2zUcO",
    "Dr. Von Fusion (gender: male)": "Mg1264PmwVoIedxsF9nu",
    "Kawaii Aerisita (gender: female)": "vGQNBgLaiM3EdZtxIiuY",
    "Lisa Kim (gender: female)": "VjguIG2t2hwOlsU1ftxC",
}

# Función para devolver el ID basado en la elección
def obtener_id(eleccion):
    return nombre_a_id.get(eleccion, "ID no encontrado")



# Crear la carpeta de salida si no existe
output_folder = '/tmp/audios'
os.makedirs(output_folder, exist_ok=True)

def eliminar_contenido_carpetas():
    carpetas = ['/tmp/audios']

    for carpeta in carpetas:
        if os.path.exists(carpeta):
            shutil.rmtree(carpeta)
            os.makedirs(carpeta)

def procesar_audio(file, continue_fragment, process_multiple):
    """Procesa uno o varios archivos MP3 y los divide en fragmentos o los guarda completos según la configuración."""
    eliminar_contenido_carpetas()

    output_folder = "/tmp/audios"  # Carpeta de salida

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    try:
        # Si es una lista de archivos
        if process_multiple:
            if not isinstance(file, list):
                return ["Por favor, carga una lista de archivos cuando 'Procesar Múltiples' esté activo."]

            output_files = []
            for audio_file in file:
                if not os.path.exists(audio_file):
                    return [f"Archivo no encontrado: {audio_file}"]

                audio = AudioSegment.from_mp3(audio_file)
                output_filename = os.path.join(output_folder, os.path.basename(audio_file))
                audio.export(output_filename, format='mp3')
                output_files.append(output_filename)

            return ["Archivos procesados y guardados en /tmp/audios:"] + output_files

        # Si es un solo archivo
        else:
            if isinstance(file, list):
                if len(file) != 1:
                    return ["Por favor, carga solo un archivo si 'Procesar Múltiples' no está activo."]
                file = file[0]  # Extraer el único archivo de la lista

            if not os.path.exists(file):
                return [f"Archivo no encontrado: {file}"]

            audio = AudioSegment.from_mp3(file)

            if continue_fragment:
                # Fragmentar el audio en segmentos de 30 segundos
                duration = 30 * 1000  # 30 segundos en milisegundos
                output_files = []

                for i, chunk in enumerate(range(0, len(audio), duration)):
                    segment = audio[chunk:chunk + duration]
                    output_filename = os.path.join(output_folder, f'{i + 1:04d}.mp3')
                    segment.export(output_filename, format='mp3')
                    output_files.append(output_filename)

                return ["Archivos fragmentados y guardados en /tmp/audios:"] + output_files
            else:
                # Guardar el audio completo
                output_filename = os.path.join(output_folder, '0001.mp3')
                audio.export(output_filename, format='mp3')
                return ["Archivo completo guardado en /tmp/audios:", output_filename]

    except Exception as e:
        return [f"Error procesando audio: {e}"]

# Función para crear el archivo .zip de la carpeta de imágenes
def create_zip_of_videos():
        # Crear el archivo zip
        zip_filename = "/tmp/Video_Compressed.zip"
        shutil.make_archive(zip_filename.replace(".zip", ""), 'zip', "/tmp/videos")  # Comprimir la carpeta

        # Devolver el archivo comprimido para ser descargado
        return zip_filename

def on_save_button_zip():
        # Llamar a la función para crear el archivo zip
        zip_file = create_zip_of_videos()

        # Devolver el archivo para que el componente gr.File pueda manejarlo
        return zip_file  # El archivo zip será devuelto al componente gr.File para su descarga


# Función para crear el archivo .zip de la carpeta de imágenes
def create_zip_of_videostts():
        # Crear el archivo zip
        zip_filename = "/tmp/tts_Video_Compressed.zip"
        shutil.make_archive(zip_filename.replace(".zip", ""), 'zip', "/tmp/videos_tts")  # Comprimir la carpeta

        # Devolver el archivo comprimido para ser descargado
        return zip_filename

def on2_save_button_zip():
        # Llamar a la función para crear el archivo zip
        zip_file = create_zip_of_videostts()

        # Devolver el archivo para que el componente gr.File pueda manejarlo
        return zip_file  # El archivo zip será devuelto al componente gr.File para su descarga
# Definir la interfaz
with gr.Blocks() as demo:
    # Título
    gr.HTML(f"<h1 style='text-align: center; font-size: 3em;'>HEDRA 4.0 - AUTOMATIC</p>Created by:<a href='https://www.youtube.com/@IA.Sistema.de.Interes' target='_blank'>IA(Sistema de Interés)</a></p>")
    
    with gr.Tabs():
        # Primera pestaña: Text to Video
        with gr.Tab("Text to Speech - Video Avatar"):
            with gr.Row():
                with gr.Column(scale=1):
                    upload_img = gr.Image(type="pil", label="Upload Image", elem_id="upload_img", interactive=True, visible=False)
                    img0 = gr.Image(type="pil", label="Avatar", elem_id="img0", interactive=False)
                    load_image_checkbox = gr.Checkbox(label="Load Image", value=False, elem_id="load_image_checkbox")
                    prompt_txt = gr.Textbox(label="Prompt", lines=4, elem_id="prompt_txt")
                    negative_prompt = gr.Checkbox(label="Negative Prompt", value=False, visible=True, elem_id="Negative")
                    negative_prompt_txt = gr.Textbox(label="Negative Prompt", placeholder="Enter text", elem_id="Negative Prompt", visible=False)
                    use_manual_seed = gr.Checkbox(label="Add Seed", value=False, visible=True, elem_id="Add_Seed")
                    seed_number = gr.Textbox(label="Seed", placeholder="Enter text", elem_id="Seed", visible=False)
                    generate_avatar_button = gr.Button("Generate Avatar", elem_id="generate_avatar_button")
                    aspect_ratio_dropdown = gr.Dropdown(choices=["16:9", "9:16", "1:1"], label="Aspect Ratio", value="16:9", elem_id="aspect_ratio_dropdown")
                    aspect_tts = gr.Dropdown(choices=["Laura (gender: female)", "John (gender: male)"], label="Text to Speech TTS", value="Laura (gender: female)", elem_id="aspect_tts")
                    audio_text = gr.Textbox(label="Audio TTS write here (maximum 300 characters)", max_length=300, lines=4, elem_id="audio_text")
                    create_button3 = gr.Button("Generate Video Avatar", elem_id="create_button3")
                    save_button0 = gr.Button("Compress all videos", elem_id="save_button3")
                    load_button = gr.Button("Load video list", elem_id="create_button3")
                
                with gr.Column(scale=2):
                    video_outputs3 = gr.Gallery([])
                    output_textbox3 = gr.Textbox(label="Output", interactive=False, elem_id="output_textbox3")
                    download_log = gr.File(label="Download Zip", elem_id="download_log")

            load_image_checkbox.change(
                lambda x: [gr.update(visible=x), gr.update(visible=not x), gr.update(visible=not x), gr.update(visible=not x), gr.update(visible=(not x and negative_prompt.value)), gr.update(visible=not x)], 
                load_image_checkbox, 
                [upload_img, img0, prompt_txt, negative_prompt, negative_prompt_txt, generate_avatar_button]
            )
            negative_prompt.change(lambda x: gr.update(visible=x), negative_prompt, negative_prompt_txt)
            use_manual_seed.change(activar_end_frame, use_manual_seed, seed_number)

            create_button3.click(
                fn=safe_execution(run_generate_tts_video),
                inputs=[prompt_txt, audio_text, aspect_ratio_dropdown, aspect_tts, use_manual_seed, seed_number],
                outputs=[video_outputs3, output_textbox3]
            )

            upload_img.change(fn=safe_execution(process_and_save_image1), inputs=[upload_img], outputs=[])
            generate_avatar_button.click(
                fn=safe_execution(run_generate_avatar),
                inputs=[prompt_txt, aspect_ratio_dropdown, negative_prompt_txt, use_manual_seed, seed_number, negative_prompt],
                outputs=[img0, output_textbox3]
            )
            load_button.click(fn=safe_execution(handle_video_output_tts), inputs=[], outputs=[video_outputs3, output_textbox3])
            save_button0.click(fn=safe_execution(on2_save_button_zip), outputs=download_log)

        # Segunda pestaña: Image+Audio to Video Avatar
        with gr.Tab("Image+Audio to Video Avatar"):
            with gr.Row():
                with gr.Column(scale=1):
                    img1 = gr.Image(type="pil", label="Drag image here or select image", interactive=True, elem_id="img1")
                    img2 = gr.Image(type="pil", label="Upload the last frame image", interactive=True, elem_id="img2", visible=False, width=200, height=200)
                    inputs_audio = gr.File(label="Sube tu archivo MP3 o lista de MP3", type="filepath", file_types=[".mp3"], file_count="multiple")
                    aspect_ratio_dropdown = gr.Dropdown(choices=["16:9", "9:16", "1:1"], label="Aspect Ratio", value="16:9", elem_id="aspect_ratio_dropdown")
                    subject = gr.Textbox(label="Prompt", placeholder="Prompt text", elem_id="description_input")
                    seed_input = gr.Checkbox(label="Seed Manual", value=False, visible=True)
                    Seed_text = gr.Textbox(label="Seed", placeholder="Enter seed", elem_id="seed_input", visible=False)
                    continue_fragment = gr.Checkbox(label="Continue Fragment", value=False, visible=False, elem_id="loop_video")
                    process_multiple = gr.Checkbox(label="Procesar múltiples archivos sin dividir", value=False)
                    prompt_upsampling = gr.Checkbox(label="prompt upsampling", value=True, visible=False, elem_id="prompt_upsampling")
                    create_button = gr.Button("Generate Video Avatar", elem_id="create_button")
                    save_button = gr.Button("Render", elem_id="save_button")
                    load_button = gr.Button("Load video list", elem_id="create_button3")
                    save_button3 = gr.Button("Compress all videos", elem_id="compress_button")
                
                with gr.Column(scale=2):
                    video_outputs = gr.Gallery([])
                    output_textbox = gr.Textbox(label="Output", interactive=False, elem_id="output_textbox")
                    download_log = gr.File(label="Download Zip", elem_id="download_log")

            inputs_audio.change(fn=safe_execution(procesar_audio), inputs=[inputs_audio, continue_fragment, process_multiple], outputs=[output_textbox])
            seed_input.change(activar_end_frame, seed_input, Seed_text)
            img1.change(fn=safe_execution(process_and_save_image1), inputs=[img1], outputs=[])
            load_button.click(fn=safe_execution(handle_video_output), inputs=[], outputs=[video_outputs, output_textbox])
            create_button.click(fn=safe_execution(run_generate_img_audio_video), inputs=[subject, aspect_ratio_dropdown, seed_input, Seed_text, continue_fragment, process_multiple], outputs=[video_outputs, output_textbox])
            save_button.click(fn=safe_execution(run_save_and_display), inputs=[], outputs=[video_outputs, output_textbox])
            save_button3.click(fn=safe_execution(on_save_button_zip), outputs=download_log)

# Ejecutar la interfaz
demo.launch(inline=False, debug=False, share=True)