import ast
import os
import importlib
import pkgutil

class VulnerabilityScanner:
    def __init__(self, modules_dir='modules'):
        self.modules_dir = modules_dir
        self.load_detectors()

    def load_detectors(self):
        self.detector_classes = []
        for _, module_name, _ in pkgutil.iter_modules([self.modules_dir]):
            try:
                module = importlib.import_module(f'modules.{module_name}')
                if hasattr(module, 'Detector'):
                    detector_class = getattr(module, 'Detector')
                    self.detector_classes.append(detector_class)
            except Exception as e:
                print(f"Error al cargar el módulo {module_name}: {e}")

    def scan_file(self, file_path, vuln_types=None):
        """
        Escanea un archivo y devuelve las vulnerabilidades encontradas.
        
        :param file_path: Ruta del archivo a analizar
        :param vuln_types: Lista de tipos de vulnerabilidad a filtrar (opcional)
        :return: Lista de vulnerabilidades: (linea, col, desc, tipo)
        """
        with open(file_path, 'r', encoding='utf-8') as file:
            try:
                tree = ast.parse(file.read(), filename=file_path)
            except SyntaxError as e:
                print(f"Error parsing {file_path}: {e}")
                return []

        vulnerabilities = []
        for detector_class in self.detector_classes:
            detector = detector_class()
            # Suponemos que cada detector retorna vulnerabilidades con un tipo
            # Ejemplo: [(line, col, desc, type), ...]
            if hasattr(detector, 'run'):
                detector_vulnerabilities = detector.run(tree)
            else:
                detector_vulnerabilities = detector.visit(tree)

            if vuln_types:
                # Filtrar por tipos solicitados
                detector_vulnerabilities = [
                    v for v in detector_vulnerabilities if v[3] in vuln_types
                ]

            if detector_vulnerabilities:
                vulnerabilities.extend(detector_vulnerabilities)

        return vulnerabilities

    def scan_directory(self, directory, vuln_types=None, ignore_list=None):
        """
        Escanea un directorio recursivamente y devuelve una lista de tuplas
        (file_path, [vulnerabilidades]) para cada archivo analizado (con o sin vulnerabilidades).
        """
        vulnerabilities = []
        ignore_set = set(ignore_list) if ignore_list else set()

        for root, _, files in os.walk(directory):
            for filename in files:
                if filename.endswith('.py'):
                    file_path = os.path.join(root, filename)

                    # Si el archivo está en la lista de ignorados, saltarlo
                    if file_path in ignore_set:
                        continue

                    vulns = self.scan_file(file_path, vuln_types=vuln_types)
                    
                    # Ahora siempre agregamos el resultado, aunque sea una lista vacía
                    vulnerabilities.append((file_path, vulns))

        return vulnerabilities
