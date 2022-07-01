import deepdream
import utils.utils as utils
from utils.constants import *

config = {
    "input": "sowa (1).jpg",
    "img_width": 750,
    "layers_to_use": ["layer4"],
    "model_name": SupportedModels.RESNET50.name,
    "pretrained_weights": SupportedPretrainedWeights.PLACES_365.name,
    "pyramid_size": 6,
    "pyramid_ratio": 1,
    "num_gradient_ascent_iterations": 10,
    "lr": 0.1,
    "use_noise": False,
    "spatial_shift_size": 80,
    "smoothing_coefficient": 0.5,
    "dump_dir": OUT_IMAGES_PATH,
    "should_display": False,
    "create_ouroboros": False,
    "ouroboros_length": 40
}

config['input_name'] = os.path.basename(config['input'])
config["dump_dir"] = os.path.join(config['dump_dir'], "places",
                                  f'{config["model_name"]}_{config["pretrained_weights"]}')

def run_script(input_files):
    config ['input'] = input_files[0]
    config['input_name'] = os.path.basename(config['input'])
    img = deepdream.deep_dream_static_image(config,
                                                    img=None)  # img=None -> will be loaded inside of deep_dream_static_image
    dump_path = utils.save_and_maybe_display_image(config, img)
    print(f'Saved DeepDream static image to: {os.path.relpath(dump_path)}\n')


def run_script_for_different_layers(layers, input_files):

    for file in input_files:
        config["input"] = file
        config['input_name'] = os.path.basename(config['input'])

        for layer in layers:

            config["layers_to_use"] = [layer]
            config['input_name'] = os.path.basename(config['input'])

            for x in range(10): #ilość iteracji dla warstwy i obrazu
                i = (x + 1) / 90 # inkrement (o jaką wartość podnosimy parametr co krok)
                config['pyramid_ratio'] = i + 1.4 # od jakiej wartości zaczyna pętla (musi być > 1) (np. i+1, i+1.1, i+1.2 itp.)
                img = deepdream.deep_dream_static_image(config,
                                                        img=None)  # img=None -> will be loaded inside of deep_dream_static_image
                dump_path = utils.save_and_maybe_display_image(config, img)
                print(f'Saved DeepDream static image to: {os.path.relpath(dump_path)}\n')
            else:
                print("Sequence finished for layer " + layer)
        else:
            print("Layer finished")
    else:
        print("Code exited successfully")


if __name__ == '__main__':
    print('Dreaming started!')

    # Here we can perform any kind of loop over configuration settings, yeah!

    input_files = ["sowa (1).png", "sowa (2).png", "sowa (3).png", "sowa (4).png", "sowa (5).png"] # obrazy do obrobienia

    layers = ["layer4", "layer3"] # warstwy

    run_script_for_different_layers(layers, input_files)

    ####################################
    # Barteńku!
    # aby zmienić wartości parametrów po których latają pętlę idź do definicji funkcji run_script_for_different_layers() 
    # i modyfikuj wartości w pętli (patrz linijka 48)
    # w razie kłopotów z pamięcią spróbuj zmniejszyć rozdzielczość (linijka 7 - wartość img_width)
    # jeśli chcesz bawić się innymi parametrami od linijki 5 zaczyna się definicja konfiguracji. 
    # 
    # Aby uruchomić ten kod wystarczy, że skorzystasz z terminala środowiska Condy z wgranymi wszystkimi gadżetami
    # do ML (tak jak to robiliśmy u Ciebie) i odpalisz ten plik tj. 'python variableAscent.py'. Wszystkie parametry kontrolujesz
    # z kodu.

    # Powodzenia!!!! <3
    # ################################### 