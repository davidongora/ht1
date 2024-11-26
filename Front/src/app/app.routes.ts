import { Routes } from '@angular/router';
import { CustomersComponent } from './home/customers/customers.component';
import { provideHttpClient } from '@angular/common/http'; // Import provideHttpClient
import { provideRouter } from '@angular/router';

export const routes: Routes = [
  
  {
    path: 'home',
    loadChildren: () => import('./home/home.module').then(m => m.HomeModule)
  },
  {
    path: 'store',
    loadChildren: () => import('./store/store.module').then(m => m.StoreModule)
  },
  { path: 'customers', component: CustomersComponent } ,// Define the route for CustomersComponent

  {
    path: '**',
    redirectTo: 'home/landing'
  },

  
];

export const appConfig = {
  providers: [
    provideRouter(routes),
    provideHttpClient() // Provide HttpClient globally
  ]
};
