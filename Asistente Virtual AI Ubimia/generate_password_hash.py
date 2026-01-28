"""
Script para generar hash de contraseña para mayor seguridad
"""
import hashlib
import getpass

def hash_password(password: str) -> str:
    """Crear hash seguro de la contraseña"""
    return hashlib.sha256(password.encode()).hexdigest()

if __name__ == "__main__":
    print("🔐 Generador de Hash de Contraseña")
    print("=" * 40)
    
    password = getpass.getpass("Ingresa la contraseña: ")
    confirm_password = getpass.getpass("Confirma la contraseña: ")
    
    if password != confirm_password:
        print("❌ Las contraseñas no coinciden")
        exit(1)
    
    if len(password) < 8:
        print("⚠️  Advertencia: Se recomienda una contraseña de al menos 8 caracteres")
    
    password_hash = hash_password(password)
    
    print("\n✅ Hash generado exitosamente:")
    print(f"APP_PASSWORD_HASH={password_hash}")
    print("\n💡 Copia esta línea a tu archivo .env y comenta APP_PASSWORD")
    print("   para mayor seguridad en producción.")