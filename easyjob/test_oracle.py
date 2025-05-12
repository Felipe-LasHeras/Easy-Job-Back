
import oracledb

# Cambia esta ruta a donde tengas instalado Oracle Instant Client
oracledb.init_oracle_client(lib_dir="Z:\Documentos\Trabajos\instantclient-basic-windows.x64-23.8.0.25.04\instantclient_23_8")

conn = oracledb.connect(user="ADMIN", dsn="sumativa_high")
print("✅ Conexión exitosa")
conn.close()
