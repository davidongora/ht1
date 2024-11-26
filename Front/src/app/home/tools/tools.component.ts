import { NgFor } from '@angular/common';
import { Component } from '@angular/core';

@Component({
  selector: 'app-tools',
  standalone: true,
  imports: [NgFor],
  templateUrl: './tools.component.html',
  styleUrl: './tools.component.css'
})
export class ToolsComponent {
  tractorStates = [
  
    { name: 'FMD ', imageUrl: 'https://ht-mobileassets.s3.amazonaws.com/tractorModels/t6090-removebg-preview.png' },
    { name: 'Sichey', imageUrl: 'https://ht-mobileassets.s3.amazonaws.com/tractorModels/TS6-125.png' },
    { name: 'CFAO ', imageUrl: 'https://ht-mobileassets.s3.amazonaws.com/tractorModels/JD_6XXXB_OOS.png' },
    { name: 'FMD Marsay Furguson dealership', imageUrl: 'https://ht-mobileassets.s3.amazonaws.com/tractorModels/DI-75-removebg-preview.png' },
    { name: 'Mascor ', imageUrl: 'https://ht-mobileassets.s3.amazonaws.com/tractorModels/Case_IH_JX90.png' },
    { name: 'CMC', imageUrl: 'https://ht-mobileassets.s3.amazonaws.com/tractorModels/Yanmar.jpg' },
    { name: ' Terranova', imageUrl: 'https://s3-us-west-2.amazonaws.com/ht-mobileassets/ti_massey_ferguson_tractor_mf5710.png' },
    
  ];
}
