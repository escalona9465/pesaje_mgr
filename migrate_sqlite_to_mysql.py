"""
Script de migracion de SQLite (pesaje.db y piezas.db) a MySQL.

Lee la configuracion desde variables de entorno (o archivo .env si existe):
  MYSQL_HOST       (default: localhost)
  MYSQL_PORT       (default: 3306)
  MYSQL_USER       (default: root)
  MYSQL_PASSWORD   (default: "")
  MYSQL_DB_PESAJE  (default: pesaje)
  MYSQL_DB_PIEZAS  (default: piezas)

Uso:
  python migrate_sqlite_to_mysql.py
  python migrate_sqlite_to_mysql.py --overwrite   # Vacia las tablas destino antes de insertar
"""

import argparse
import os
import sqlite3
import sys
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_PESAJE_SQLITE = os.path.join(BASE_DIR, "components", "database", "pesaje.db")
DEFAULT_PIEZAS_SQLITE = os.path.join(BASE_DIR, "components", "database", "piezas.db")

PESAJE_DDL = {
    "clientes": """
        CREATE TABLE IF NOT EXISTS `clientes` (
            `id` INT NOT NULL,
            `codigo` VARCHAR(50) NOT NULL,
            `cliente` VARCHAR(100) NOT NULL,
            `descripcion` TEXT,
            INDEX `idx_clientes_id` (`id`),
            INDEX `idx_clientes_codigo` (`codigo`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """,
    "bobinas": """
        CREATE TABLE IF NOT EXISTS `bobinas` (
            `op` BIGINT NOT NULL,
            `tara` DOUBLE NOT NULL,
            `paletas_total` INT NOT NULL,
            `bobinas_paleta` INT NULL,
            `paleta_actual` INT NOT NULL,
            `matriz` VARCHAR(20) NOT NULL,
            `hablador` VARCHAR(20) NOT NULL,
            `total_op` VARCHAR(50) NOT NULL,
            `codigo` VARCHAR(50) NOT NULL,
            INDEX `idx_bobinas_op` (`op`),
            INDEX `idx_bobinas_codigo` (`codigo`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """,
    "habladores": """
        CREATE TABLE IF NOT EXISTS `habladores` (
            `op` BIGINT NOT NULL,
            `cantidad` DOUBLE NOT NULL,
            `posicion` INT NULL,
            `observacion` TEXT NOT NULL,
            `producto` TEXT NOT NULL,
            INDEX `idx_habladores_op` (`op`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """,
    "usuarios": """
        CREATE TABLE IF NOT EXISTS `usuarios` (
            `id` INT NOT NULL,
            `cedula` BIGINT NOT NULL,
            `usuario` VARCHAR(100) NOT NULL,
            `nombre` VARCHAR(100) NOT NULL,
            `apellido` VARCHAR(100) NOT NULL,
            `ficha` INT NOT NULL,
            `password` VARCHAR(100) NOT NULL,
            `email` VARCHAR(100) NOT NULL,
            `nivel` VARCHAR(50) NOT NULL,
            `turno` VARCHAR(50) NOT NULL,
            `supervisor` VARCHAR(50),
            INDEX `idx_usuarios_id` (`id`),
            INDEX `idx_usuarios_nivel` (`nivel`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """,
    "config_proceso": """
        CREATE TABLE IF NOT EXISTS `config_proceso` (
            `server_ip` VARCHAR(50) NOT NULL,
            `server_port` VARCHAR(20) NOT NULL,
            `server_usr` VARCHAR(50) NOT NULL,
            `server_pw` VARCHAR(50) NOT NULL,
            `printer1_name` VARCHAR(100) NOT NULL,
            `printer2_name` VARCHAR(100) NOT NULL,
            `data_source_type` VARCHAR(50) NOT NULL,
            `com_port1` VARCHAR(50) NOT NULL,
            `com_port2` VARCHAR(50) NOT NULL,
            `mode_b1` INT,
            `mode_b2` INT,
            `mode_adobe` INT,
            `path_adobe` TEXT,
            `key` VARCHAR(50) NOT NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """,
    "reports": """
        CREATE TABLE IF NOT EXISTS `reports` (
            `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
            `exception` TEXT,
            `descripcion` TEXT,
            `datos` TEXT,
            `fecha` VARCHAR(50),
            `operador` VARCHAR(100)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """,
    "paletas": """
        CREATE TABLE IF NOT EXISTS `paletas` (
            `id` INT NOT NULL,
            `nombre` VARCHAR(100) NOT NULL,
            `peso` DOUBLE NOT NULL,
            INDEX `idx_paletas_id` (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """,
    "proceso_bobina": """
        CREATE TABLE IF NOT EXISTS `proceso_bobina` (
            `ticket` BIGINT NOT NULL,
            `peso_bruto` DOUBLE NOT NULL,
            `peso_neto` DOUBLE NOT NULL,
            `n_paleta` INT NOT NULL,
            `bobina_matriz` VARCHAR(20) NOT NULL,
            `fecha_emision` VARCHAR(20) NOT NULL,
            `op` BIGINT NOT NULL,
            `ficha` INT NOT NULL,
            `hora` VARCHAR(20),
            `bobina` INT,
            `aprobado_por` VARCHAR(50),
            INDEX `idx_pb_ticket` (`ticket`),
            INDEX `idx_pb_op` (`op`),
            INDEX `idx_pb_op_paleta` (`op`, `n_paleta`),
            INDEX `idx_pb_fecha` (`fecha_emision`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """,
    "proceso_bobina_eliminados": """
        CREATE TABLE IF NOT EXISTS `proceso_bobina_eliminados` (
            `ticket` BIGINT NOT NULL,
            `peso_bruto` DOUBLE NOT NULL,
            `peso_neto` DOUBLE NOT NULL,
            `n_paleta` INT NOT NULL,
            `bobina_matriz` VARCHAR(20) NOT NULL,
            `fecha_emision` VARCHAR(20) NOT NULL,
            `op` BIGINT NOT NULL,
            `ficha` INT NOT NULL,
            `hora` VARCHAR(20),
            `bobina` INT,
            `aprobado_por` VARCHAR(50),
            INDEX `idx_pbe_op_paleta` (`op`, `n_paleta`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """,
    "productos": """
        CREATE TABLE IF NOT EXISTS `productos` (
            `codigo_producto` VARCHAR(50) NOT NULL,
            `producto` VARCHAR(100) NOT NULL,
            `peso_max` DOUBLE NULL,
            `cliente_id` INT,
            `peso_min` DOUBLE NULL,
            INDEX `idx_productos_codigo` (`codigo_producto`),
            INDEX `idx_productos_cliente` (`cliente_id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """,
}

PIEZAS_DDL = {
    "proceso_pieza": """
        CREATE TABLE IF NOT EXISTS `proceso_pieza` (
            `ticket` BIGINT NOT NULL,
            `neto` DOUBLE NOT NULL,
            `n_bulto` INT NOT NULL,
            `n_caja` INT NOT NULL,
            `n_paleta` INT,
            `fecha_emision` VARCHAR(20) NOT NULL,
            `op` BIGINT NOT NULL,
            `ficha` INT NOT NULL,
            `hora` VARCHAR(20),
            `piezas` INT,
            `paquetes` INT,
            INDEX `idx_pp_ticket` (`ticket`),
            INDEX `idx_pp_op` (`op`),
            INDEX `idx_pp_op_caja` (`op`, `n_caja`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """,
    "proceso_pieza_eliminados": """
        CREATE TABLE IF NOT EXISTS `proceso_pieza_eliminados` (
            `ticket` BIGINT NOT NULL,
            `neto` DOUBLE NOT NULL,
            `n_bulto` INT NOT NULL,
            `n_caja` INT NOT NULL,
            `n_paleta` INT,
            `fecha_emision` VARCHAR(20) NOT NULL,
            `op` BIGINT NOT NULL,
            `ficha` INT NOT NULL,
            `hora` VARCHAR(20),
            `piezas` INT,
            INDEX `idx_ppe_op` (`op`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """,
    "piezas": """
        CREATE TABLE IF NOT EXISTS `piezas` (
            `op` BIGINT NOT NULL,
            `bultos_total` INT NOT NULL,
            `pieza_bulto` INT NOT NULL,
            `bulto_actual` INT NOT NULL,
            `caja_actual` INT NOT NULL,
            `paleta_total` INT NOT NULL,
            `codigo` VARCHAR(50) NOT NULL,
            `paquetes` INT,
            INDEX `idx_piezas_op` (`op`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """,
}


def get_mysql_connection(database=None):
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        port=int(os.getenv("MYSQL_PORT", "3306")),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", ""),
        database=database,
        charset="utf8mb4",
        autocommit=False,
    )


NUMERIC_NULLABLE_COLUMNS = {
    "bobinas": {"bobinas_paleta"},
    "habladores": {"posicion"},
    "productos": {"peso_max", "peso_min"},
}


def sanitize_batch(table_name, col_names, batch):
    target_cols = NUMERIC_NULLABLE_COLUMNS.get(table_name)
    if not target_cols:
        return batch
    target_indices = [i for i, c in enumerate(col_names) if c in target_cols]
    if not target_indices:
        return batch
    cleaned = []
    for row in batch:
        row_list = list(row)
        for idx in target_indices:
            if isinstance(row_list[idx], str) and row_list[idx].strip() == "":
                row_list[idx] = None
        cleaned.append(tuple(row_list))
    return cleaned


def migrate_database(sqlite_path, mysql_db_name, ddl_map, overwrite=False, batch_size=5000):
    if not os.path.exists(sqlite_path):
        print(f"[ERROR] No se encontro el archivo SQLite: {sqlite_path}")
        return False

    print(f"\n=== Migrando {sqlite_path} -> MySQL '{mysql_db_name}' ===")

    # 1. Crear base de datos en MySQL si no existe
    admin_conn = get_mysql_connection()
    admin_cur = admin_conn.cursor()
    admin_cur.execute(
        f"CREATE DATABASE IF NOT EXISTS `{mysql_db_name}` "
        "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
    )
    admin_conn.commit()
    admin_cur.close()
    admin_conn.close()

    # 2. Conectar a SQLite y a la BD destino en MySQL
    sq_conn = sqlite3.connect(sqlite_path)
    sq_cur = sq_conn.cursor()

    my_conn = get_mysql_connection(mysql_db_name)
    my_cur = my_conn.cursor()

    all_ok = True
    for table_name, create_sql in ddl_map.items():
        if overwrite:
            my_cur.execute(f"DROP TABLE IF EXISTS `{table_name}`")
            my_conn.commit()
        my_cur.execute(create_sql)
        my_conn.commit()

        my_cur.execute(f"SELECT COUNT(*) FROM `{table_name}`")
        existing_rows = my_cur.fetchone()[0]

        sq_cur.execute(f'SELECT COUNT(*) FROM "{table_name}"')
        total_sqlite = sq_cur.fetchone()[0]

        if existing_rows > 0 and not overwrite:
            print(
                f"  [OMITIDA] {table_name}: ya tiene {existing_rows} filas en MySQL "
                f"(SQLite: {total_sqlite}). Usa --overwrite para reemplazar."
            )
            continue

        if total_sqlite == 0:
            print(f"  [OK] {table_name}: 0 filas (tabla vacia).")
            continue

        cols_info = sq_cur.execute(f'PRAGMA table_info("{table_name}")').fetchall()
        col_names = [c[1] for c in cols_info]
        cols_sql = ", ".join(f"`{c}`" for c in col_names)
        placeholders = ", ".join(["%s"] * len(col_names))
        insert_sql = f"INSERT INTO `{table_name}` ({cols_sql}) VALUES ({placeholders})"

        sq_cur.execute(f'SELECT { ", ".join(chr(34)+c+chr(34) for c in col_names) } FROM "{table_name}"')
        migrated = 0
        while True:
            batch = sq_cur.fetchmany(batch_size)
            if not batch:
                break
            batch = sanitize_batch(table_name, col_names, batch)
            my_cur.executemany(insert_sql, batch)
            my_conn.commit()
            migrated += len(batch)
            print(f"  -> {table_name}: {migrated}/{total_sqlite} filas...", end="\r")

        my_cur.execute(f"SELECT COUNT(*) FROM `{table_name}`")
        final_mysql = my_cur.fetchone()[0]
        status = "OK" if final_mysql == total_sqlite else "MISMATCH"
        if status != "OK":
            all_ok = False
        print(f"  [{status}] {table_name}: SQLite={total_sqlite}, MySQL={final_mysql}        ")

    sq_cur.close()
    sq_conn.close()
    my_cur.close()
    my_conn.close()
    return all_ok


def main():
    parser = argparse.ArgumentParser(description="Migrar SQLite (pesaje.db y piezas.db) a MySQL.")
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Vacia (TRUNCATE) las tablas en MySQL antes de insertar los datos.",
    )
    parser.add_argument("--pesaje-sqlite", default=DEFAULT_PESAJE_SQLITE, help="Ruta a pesaje.db")
    parser.add_argument("--piezas-sqlite", default=DEFAULT_PIEZAS_SQLITE, help="Ruta a piezas.db")
    args = parser.parse_args()

    pesaje_db = os.getenv("MYSQL_DB_PESAJE", "pesaje")
    piezas_db = os.getenv("MYSQL_DB_PIEZAS", "piezas")

    try:
        ok1 = migrate_database(args.pesaje_sqlite, pesaje_db, PESAJE_DDL, overwrite=args.overwrite)
        ok2 = migrate_database(args.piezas_sqlite, piezas_db, PIEZAS_DDL, overwrite=args.overwrite)
    except mysql.connector.Error as err:
        print(f"\n[ERROR MySQL] {err}")
        sys.exit(1)

    if ok1 and ok2:
        print("\nMigracion completada exitosamente.")
    else:
        print("\nMigracion finalizada con advertencias. Revisa los conteos arriba.")
        sys.exit(1)


if __name__ == "__main__":
    main()
