def validar_identificador(texto_input):
    #Esta funcion se va a encargar de validar si es V-, E- y J-

    texto = texto_input.upper().strip()
    prefijos = ["V-", "E-", "J-"]

    #Aqui se va a verificar el prefijo
    tipo_detectado = None
    for prefijo in prefijos:
        if texto.startswith(prefijo):
            tipo_detectado = prefijo
            break
    
    if not tipo_detectado:
        return False, None, None, "Error: Usa el formato V-, E- o J- seguido del numero del documento."
    
    #Aqui se va a verificar que lo demas sean numeros

    numero_doc = texto.replace(tipo_detectado, "")

    if not numero_doc.isdigit():
        return False, None, None, "Error! Despues del guion solo van numeros"
    
    #Validaciones especificas dependiendo del tipo del documento

    if tipo_detectado == "J-":
        if len(numero_doc) != 10:
            return False, None, None, f"Error!: El RIF debe tener 10 digitos (escribiste {len(numero_doc)})"
        
    else:
        if not (7 <= len(numero_doc) <= 9):
            return False, None, None, "Error! la decula debe de tener entre 7 y 9 digitos"
            
    return True, tipo_detectado.replace("-", ""), numero_doc, "OK"