/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'dev-132ehov1.us', // the auth0 domain prefix
    audience: 'casting-agency', // the audience set for the auth0 app
    clientId: 'hA1MGqI55aaxG6w7XbRCStaT4He8gTQA', // the client id generated for the auth0 app
    callbackURL: 'http://127.0.0.1:8100', // the base url of the running ionic application. 
  }
};
