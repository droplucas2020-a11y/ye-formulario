/**
 * YE | Jovens Empreendedores — receptor das respostas do formulário de entrada.
 *
 * Como usar:
 *  1. Crie uma planilha no Google Sheets.
 *  2. Extensões > Apps Script. Apague tudo e cole este arquivo.
 *  3. Implantar > Nova implantação > App da Web
 *       Executar como:      Eu
 *       Quem pode acessar:  Qualquer pessoa
 *  4. Copie a URL /exec e cole em CONFIG.endpoint no index.html
 *
 * Cada envio vira uma linha. O cabeçalho é criado na primeira resposta e
 * novas perguntas viram colunas novas automaticamente.
 */

var ABA = 'Respostas';

function doPost(e) {
  var lock = LockService.getScriptLock();
  lock.waitLock(30000); // evita duas respostas simultâneas escreverem na mesma linha

  try {
    var dados = JSON.parse(e.postData.contents);
    var planilha = SpreadsheetApp.getActiveSpreadsheet();
    var aba = planilha.getSheetByName(ABA) || planilha.insertSheet(ABA);

    // Cabeçalho: cria na primeira vez, complementa se surgirem campos novos.
    var cabecalho = aba.getLastRow() > 0
      ? aba.getRange(1, 1, 1, aba.getLastColumn()).getValues()[0]
      : [];

    var novas = Object.keys(dados).filter(function (k) {
      return cabecalho.indexOf(k) === -1;
    });

    if (novas.length) {
      cabecalho = cabecalho.concat(novas);
      aba.getRange(1, 1, 1, cabecalho.length).setValues([cabecalho]);
      aba.getRange(1, 1, 1, cabecalho.length)
         .setFontWeight('bold')
         .setBackground('#1A2029')
         .setFontColor('#D4AF37');
      aba.setFrozenRows(1);
    }

    var linha = cabecalho.map(function (coluna) {
      return dados[coluna] !== undefined ? dados[coluna] : '';
    });
    aba.appendRow(linha);

    notificar(dados);

    return resposta({ ok: true });

  } catch (erro) {
    console.error(erro);
    return resposta({ ok: false, erro: String(erro) });

  } finally {
    lock.releaseLock();
  }
}

/**
 * Avisa por e-mail a cada nova inscrição.
 * Coloque seu e-mail em DESTINO — deixe '' para desligar o aviso.
 */
var DESTINO = '';

function notificar(dados) {
  if (!DESTINO) return;

  var nome = dados['1_nome'] || 'Sem nome';
  var corpo =
    'Nova inscrição no YE\n\n' +
    'Nome: ' + nome + '\n' +
    'Idade: ' + (dados['2_idade'] || '-') + '\n' +
    'WhatsApp: ' + (dados['3_telefone'] || '-') + '\n' +
    'Instagram: ' + (dados['4_instagram'] || '-') + '\n' +
    'Cidade: ' + (dados['5_cidade'] || '-') + '\n' +
    'Atuação: ' + (dados['6_atuacao'] || '-') + '\n' +
    'Empresa: ' + (dados['7_empresa'] || '-') + '\n' +
    'Como conheceu: ' + (dados['17_conheceu'] || '-') +
      (dados['17_indicado_por'] ? ' (' + dados['17_indicado_por'] + ')' : '') + '\n\n' +
    'Respostas completas na planilha.';

  MailApp.sendEmail(DESTINO, 'YE — nova inscrição: ' + nome, corpo);
}

function resposta(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}

/** Permite abrir a URL no navegador só para conferir se está no ar. */
function doGet() {
  return ContentService.createTextOutput('YE — receptor ativo.');
}
