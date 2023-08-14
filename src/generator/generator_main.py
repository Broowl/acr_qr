from pathlib import Path
import argparse
from datetime import datetime
from generator_lib.persistence import Persistence, PersistedValues
from generator_lib.config import Config
from generator_lib.gui import GeneratorGui
from generator_lib.generator import Generator


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--out_dir")
    parser.add_argument("-k", "--key_dir")
    parser.add_argument("-e", "--event_name")
    parser.add_argument("-d", "--event_date",
                        help="date in the format yyyy-mm-dd")
    parser.add_argument("-n", "--num_codes")
    parsed_args = parser.parse_args()

    default_dir = Path.home() / "Documents" / "ACR_QR_Generator"
    out_dir = default_dir / "Codes"
    key_dir = default_dir / "Keys"
    config_path = default_dir / "config.json"
    event_name: str = ""
    event_date = datetime.today().date()
    num_codes: int = 100
    persistence = Persistence(config_path, PersistedValues(out_dir))
    out_dir = persistence.get_persisted_out_dir()
    if parsed_args.out_dir is not None:
        out_dir = Path(parsed_args.out_dir)
        persistence.persist_out_dir(out_dir)
    if parsed_args.key_dir is not None:
        key_dir = Path(parsed_args.key_dir)
    if parsed_args.event_name is not None:
        event_name = parsed_args.event_name
    if parsed_args.event_date is not None:
        event_date = datetime.strptime(
            parsed_args.event_date, '%y-%m-%d').date()
    if parsed_args.num_codes is not None:
        num_codes = parsed_args.num_codes

    initial_config = Config(event_name, event_date,
                            num_codes, out_dir, key_dir)

    gui = GeneratorGui(initial_config)
    progress_indicator = gui.get_progress_indicator()
    generator = Generator(progress_indicator)

    gui.set_generator(generator.generate)
    gui.set_out_dir_listener(persistence.persist_out_dir)
    gui.run()


if __name__ == "__main__":
    main()
