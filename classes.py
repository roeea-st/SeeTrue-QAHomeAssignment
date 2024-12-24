from datetime import datetime

class App:

    def __init__(self, bag_image_dir):
        self.bag_image_dir = bag_image_dir
        self.detectors = {}
        self.screened_bags_counter = 0

    def add_detector(self, name, detector):
        self.detectors[name] = detector

    def get_screened_bags_amount(self):
        return self.screened_bags_counter

    def screen_next_bag(self):
        screening_event = ScreeningEvent()
        bag = Bag(f'{self.bag_image_dir}/bag.png', screening_event)
        screening_event.set_associated_bag(bag)
        for detector_name, detector in self.detectors.items():
            if detector.detect_threat(bag):
                print(f'Threat Alarm! - {detector_name} detected.')
                bag.add_threat(detector_name)
        self.screened_bags_counter += 1


class Bag:
    def __init__(self, image_path, parent_screening_event):
        with open(image_path, 'rb') as file:
            self.raw_image = file.read()
        self.threats = []
        self.parent_screening_event = parent_screening_event

    def add_threat(self, threat_name):
        self.threats.append(threat_name)


class ScreeningEvent:
    def __init__(self):
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.bag = None
    def set_associated_bag(self, bag):
        self.bag = bag


class KnifeDetector:
    def detect_threat(self, bag):
        # Some AI magic on bag... No threat - returning False
        return False

class PistolDetector:
    def detect_threat(self, bag):
        # Some AI magic on bag... No threat - returning False
        return False

class BombDetector:
    def detect_threat(self, bag):
        # Some AI magic on bag... No threat - returning False
        return False

