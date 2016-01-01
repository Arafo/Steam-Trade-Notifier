// File name: SteamTradeNotifier.gs
// Author: Rafa Marcen
// Date created: 26/10/2014
// Date last modified: 26/10/2014
// Purpose: Send an e-mail notification when a Steam trade offer is accepted or
// received.
// Documentation URL:
// https://developer.valvesoftware.com/wiki/Steam_Web_API/IEconService

var STEAM_API_KEY = 'YOUR_STEAM_API_KEY'
var STEAM_PROFILE = 'YOUR_STEAM_PROFILE_NAME'
var RECIPIENT_ADDRESS = 'YOUR_EMAIL'
var DEBUG = false;

function obtenerTrades(service, method, version, key, userId, timeStamp) {
  var url = 'https://api.steampowered.com/'+service+'/'+method+'/v'+version+'/?key='+key+'&format=json&time_last_visit='+timeStamp;
  // If a User ID was given
  if (userId != null) {
    url += '&steamid=' + userId;
  }
  // Specify JSON as the format
  url += '&format=json';        
  if (DEBUG) {
    Logger.log(url); 
  }
  var response = UrlFetchApp.fetch(url);
  if (DEBUG) {
    Logger.log(response);
  }
  var respuesta = JSON.parse(response.getContentText()); 
  return respuesta.response;
 }

function crearCorreo(respuesta) {
  var ofertasPendientes = respuesta['pending_received_count'];
  var ofertasNuevas = respuesta['new_received_count'];
  var body = '';
  
  if (ofertasNuevas > 0) {
    body += ofertasNuevas+' nueva oferta';
    if (ofertasNuevas != 1) {
      body += 's';
    }
    body += '\r\n'
  }
  
  if (ofertasPendientes > 0) {
    body += ofertasPendientes+' oferta';
    if (ofertasPendientes != 1) {
      body += 's pendientes\r\n';
    } 
    else {
      body += ' pendiente\r\n';
    }
  }

  if (body != '') {
    body += '\r\n';
    body += 'https://steamcommunity.com/id/' + STEAM_PROFILE + '/tradeoffers/';
    return body;
  } 
  else {
    return null;
  }
}

function enviarCorreo(to, subject, body) {
  MailApp.sendEmail(to, subject, body);
}

function main() {
  var timeStamp = new Date().getTime() - (6 * 60000);
  var response = obtenerTrades('IEconService',
                       'GetTradeOffersSummary', '1',
                       STEAM_API_KEY, null, timeStamp);
  
  var body = crearCorreo(response);
  if (body != null) {
    enviarCorreo(RECIPIENT_ADDRESS, 'Steam Trade Notification', body);
  }
}