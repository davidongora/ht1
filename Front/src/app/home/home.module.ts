import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { HomeRoutingModule } from './home-routing.module';
import { GoogleMapsModule } from '@angular/google-maps';
// import { HttpClientModule } from '@angular/common/http'; // <-- Import HttpClientModule


@NgModule({
  declarations: [],
  imports: [
    CommonModule,
    HomeRoutingModule,
    GoogleMapsModule,

    // NgModule,
    // HttpClientModule
  ]
})
export class HomeModule { }
