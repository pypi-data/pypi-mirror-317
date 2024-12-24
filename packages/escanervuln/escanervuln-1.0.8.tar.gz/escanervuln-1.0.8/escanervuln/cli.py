# cli.py

import argparse
import os
import sys
import json
from .vuln_scanner import VulnerabilityScanner

VERSION = "1.0.0"

def main():
    parser = argparse.ArgumentParser(
        description='Librería Modular de Detección de Vulnerabilidades en Python'
    )
    parser.add_argument('path', help='Archivo o directorio a analizar')
    parser.add_argument('--verbose', action='store_true', help='Muestra información detallada durante el análisis')
    parser.add_argument('--quiet', action='store_true', help='Minimiza la salida en pantalla')
    parser.add_argument('--output-format', choices=['text', 'json'], default='text',
                        help='Formato de salida. Opciones: text, json (por defecto: text)')
    parser.add_argument('--output-file', help='Archivo en el que se guardará el reporte de vulnerabilidades')
    parser.add_argument('--type', action='append', dest='vuln_types',
                        help='Tipo(s) de vulnerabilidades a analizar. Puede usarse varias veces. Ej: --type xss --type rce')
    parser.add_argument('--ignore', action='append', dest='ignore_list',
                        help='Ruta(s) o patrones a ignorar. Puede usarse varias veces.')
    parser.add_argument('--exit-code-on-vulns', action='store_true',
                        help='Retorna código de salida 1 si se encuentran vulnerabilidades')
    parser.add_argument('--version', action='store_true', help='Muestra la versión de la herramienta y finaliza')

    args = parser.parse_args()

    # Si se pide la versión, se muestra y se sale.
    if args.version:
        print(f"Versión de la herramienta: {VERSION}")
        sys.exit(0)

    # Crear instancia del escáner
    scanner = VulnerabilityScanner()

    # Comprobamos si la ruta es válida
    if not os.path.exists(args.path):
        print('La ruta especificada no existe. Por favor, verifique su ruta.')
        sys.exit(1)

    # Si es archivo
    if os.path.isfile(args.path):
        if args.verbose and not args.quiet:
            print(f"[INFO] Analizando archivo: {args.path}")
        vulnerabilities = scanner.scan_file(args.path, vuln_types=args.vuln_types)
        results = []
        if vulnerabilities:
            if not args.quiet:
                print(f'Vulnerabilidades encontradas en {args.path}:')
            for vuln in vulnerabilities:
                # vuln: (linea, columna, descripcion)
                line, col, desc = vuln
                if not args.quiet:
                    print(f'Línea {line}:{col} - {desc}')
                results.append({
                    "file": args.path,
                    "line": line,
                    "column": col,
                    "description": desc
                })
            summary = {"files_analyzed": 1, "vulnerabilities_found": len(vulnerabilities)}
        else:
            if not args.quiet:
                print(f'No se encontraron vulnerabilidades en {args.path}.')
            summary = {"files_analyzed": 1, "vulnerabilities_found": 0}

    # Si es directorio
    elif os.path.isdir(args.path):
        if args.verbose and not args.quiet:
            print(f"[INFO] Analizando directorio: {args.path}")
        vulnerabilities = scanner.scan_directory(args.path, vuln_types=args.vuln_types, ignore_list=args.ignore_list)
        # vulnerabilities se asume que es lista de (file_path, [(line, col, desc), ...])
        results = []
        total_files = 0
        total_vulns = 0
        if vulnerabilities:
            # vulnerabilities podría ser una lista vacía si no se encontró nada
            # en caso de encontrar vulnerabilidades, iteramos
            for file_path, vulns_in_file in vulnerabilities:
                total_files += 1
                if vulns_in_file:
                    if not args.quiet:
                        print(f'\nVulnerabilidades encontradas en {file_path}:')
                    for vuln in vulns_in_file:
                        line, col, desc = vuln
                        total_vulns += 1
                        if not args.quiet:
                            print(f'Línea {line}:{col} - {desc}')
                        results.append({
                            "file": file_path,
                            "line": line,
                            "column": col,
                            "description": desc
                        })
                else:
                    if args.verbose and not args.quiet:
                        print(f'\nNo se encontraron vulnerabilidades en {file_path}.')
            # Puede que el escáner devuelva también archivos sin vulnerabilidades
            # Contemos todos los archivos analizados:
            # Asumimos que scanner.scan_directory devuelve todos los archivos analizados
            summary = {"files_analyzed": len(vulnerabilities), "vulnerabilities_found": total_vulns}
        else:
            # Significa que no se analizó o no se encontraron archivos, o no hay vulnerabilidades
            summary = {"files_analyzed": 0, "vulnerabilities_found": 0}
            if not args.quiet:
                print(f'No se encontraron vulnerabilidades en {args.path}.')

    # Mostrar resumen final (si no quiet)
    if not args.quiet:
        print("\n--- Resumen del análisis ---")
        print(f"Archivos analizados: {summary['files_analyzed']}")
        print(f"Vulnerabilidades encontradas: {summary['vulnerabilities_found']}")

    # Formatear salida si es JSON
    if args.output_format == 'json':
        output_data = {
            "summary": summary,
            "results": results
        }
        output_str = json.dumps(output_data, indent=2)
    else:
        # Formato texto
        # Mostrar al final sólo si no es quiet
        # Si es quiet y no se encontraron vulnerabilidades, no hay mucho por imprimir
        # Pero el summary ya se mostró arriba (si no quiet)
        # En caso quiet + text, no repetimos, ya se imprimió lo mínimo arriba
        # Si se quiere imprimir algo adicional, se podría aquí.
        output_str = None

    # Guardar resultado en archivo si se especificó
    if args.output_file:
        if args.output_format == 'json':
            with open(args.output_file, 'w', encoding='utf-8') as f:
                f.write(output_str)
        else:
            # En formato texto, regeneramos una salida coherente
            with open(args.output_file, 'w', encoding='utf-8') as f:
                f.write("Resumen del análisis:\n")
                f.write(f"Archivos analizados: {summary['files_analyzed']}\n")
                f.write(f"Vulnerabilidades encontradas: {summary['vulnerabilities_found']}\n\n")
                for r in results:
                    f.write(f"{r['file']} - Línea {r['line']}:{r['column']} - {r['description']}\n")

    else:
        # Si se eligió JSON y no quiet, imprimir en pantalla
        if args.output_format == 'json' and not args.quiet:
            print("\n--- Salida en JSON ---")
            print(output_str)

    # Salida con error si se encuentran vulnerabilidades y se solicita
    if args.exit_code_on_vulns and summary['vulnerabilities_found'] > 0:
        sys.exit(1)

    sys.exit(0)


if __name__ == '__main__':
    main()
