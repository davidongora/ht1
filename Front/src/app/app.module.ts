import { NgModule, CUSTOM_ELEMENTS_SCHEMA, NO_ERRORS_SCHEMA } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { HttpClientModule, HttpClient, HTTP_INTERCEPTORS } from '@angular/common/http';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';

// Components
import { AppComponent } from './app.component';
import { SwUpdate } from '@angular/service-worker';
import { GoogleMapsModule } from '@angular/google-maps';

// Interceptors
// import { ErrorInterceptor } from './core/helpers/error.interceptor';
// import { JwtInterceptor } from './core/helpers/jwt.interceptor';

// Import TranslateModule for internationalization if needed
// import { TranslateModule, TranslateLoader } from '@ngx-translate/core';
// import { TranslateHttpLoader } from '@ngx-translate/http-loader';

// If you have environment-specific configurations
// import { environment } from '../environments/environment';
// import { initFirebaseBackend } from './authUtils';

// Define the function to create the translate loader
// export function createTranslateLoader(http: HttpClient): TranslateHttpLoader {
//   return new TranslateHttpLoader(http, 'assets/i18n/', '.json');
// }

// Initialize Firebase backend if environment specifies
// if (environment.defaultauth === 'firebase') {
//   initFirebaseBackend(environment.firebaseConfig);
// }

// Define the NgModule
@NgModule({
  declarations: [
    // AppComponent,
    // Declare other components here
  ],
  imports: [
    BrowserModule,
    GoogleMapsModule,
    BrowserAnimationsModule,
    HttpClientModule,
    FormsModule,
    ReactiveFormsModule,
    // Import other modules here
    // TranslateModule.forRoot({
    //   loader: {
    //     provide: TranslateLoader,
    //     useFactory: createTranslateLoader,
    //     deps: [HttpClient]
    //   }
    // })
  ],
  providers: [
    // { provide: HTTP_INTERCEPTORS, useClass: JwtInterceptor, multi: true },
    // { provide: HTTP_INTERCEPTORS, useClass: ErrorInterceptor, multi: true },
    // Provide other services here
  ],
  schemas: [CUSTOM_ELEMENTS_SCHEMA, NO_ERRORS_SCHEMA],
  // bootstrap: [AppComponent]
})
export class AppModule { 
  constructor(private swUpdate: SwUpdate) {
  }

  ngOnInit() {

      if (this.swUpdate.isEnabled) {
          this.swUpdate.versionUpdates.subscribe(() => {

              if(confirm("New version available. Load New Version?")) {

                  window.location.reload();
              }
          });
      }        
  }
}
