from django.shortcuts import render
from Bio.Blast import NCBIWWW, NCBIXML
import re
from decimal import Decimal, InvalidOperation

def detect_sequence_type(sequence):
    cleaned_sequence = re.sub(r'[^a-zA-Z]', '', sequence)
    nucleotide_count = sum(cleaned_sequence.count(n) for n in ['A', 'C', 'G', 'T'])
    nucleotide_percentage = (nucleotide_count / len(cleaned_sequence)) * 100
    nucleotide_threshold = 80

    if nucleotide_percentage >= nucleotide_threshold:
        return 'nt'
    else:
        return 'nr'

def aplicaciones(request):
    return render(request, 'aplicaciones/vistablast.html')

def blast(request):
    if request.method == 'POST':
        sequence = request.POST.get('sequence')
        fasta_file = request.FILES.get('fasta_file')
        blast_type = request.POST.get('blast_type', 'blastn')

        if fasta_file:
            sequence = fasta_file.read().decode()

        if not sequence:
            return render(request, 'vistablast.html', {'error': 'Por favor, proporciona una secuencia o un archivo FASTA.'})

        sequence_type = detect_sequence_type(sequence)

        if (blast_type in ['blastn', 'tblastx'] and sequence_type != 'nt') or \
           (blast_type in ['blastp', 'tblastn', 'blastx'] and sequence_type != 'nr'):
            return render(request, 'aplicaciones/vistablast.html', {'error': 'La secuencia proporcionada no coincide con el tipo de búsqueda seleccionado.'})

        try:
            result_handle = NCBIWWW.qblast(blast_type, sequence_type, sequence)
            blast_records = NCBIXML.parse(result_handle)
            record = next(blast_records)
            alignments = []
            for alignment in record.alignments:
                for hsp in alignment.hsps:
                    ncbi_id = "N/A"
                    ncbi_id_search = re.search(r'gi\|(\d+)\|', alignment.title)
                    if ncbi_id_search:
                        ncbi_id = ncbi_id_search.group(1)
                    else:
                        protein_id_search = re.search(r'(ref|pdb|gb|emb)\|([^|]+)\|', alignment.title)
                        if protein_id_search:
                            ncbi_id = protein_id_search.group(2)

                    try:
                        e_value_formatted = "{:.2e}".format(Decimal(hsp.expect))
                    except InvalidOperation:
                        e_value_formatted = str(hsp.expect)

                    align_info = {
                        'title': alignment.title,
                        'length': alignment.length,
                        'score': hsp.score,
                        'e_value': e_value_formatted,
                        'ncbi_id': ncbi_id
                    }
                    alignments.append(align_info)
        except Exception as e:
            return render(request, 'aplicaciones/vistablast.html', {'error': f'Ocurrió un error al realizar la búsqueda de BLAST: {e}'})

        return render(request, 'resultado/resultado.html', {'alignments': alignments, 'sequence_type': sequence_type})

    return render(request, 'aplicaciones/vistablast.html')
