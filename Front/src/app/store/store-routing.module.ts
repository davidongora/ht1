import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { FilterComponent } from './filter/filter.component';
import { FeaturesComponent } from './features/features.component';

const routes: Routes = [
  {
    path: 'filter',
    component: FilterComponent
  },
  {
    path: 'features',
    component: FeaturesComponent
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class StoreRoutingModule { 

  public gender: any[] = ['Male', 'Female']
  public AgeGroup: any[] = ['Adult', 'Children']
  public price? : number
  public sixe: any[] = ['Small', 'Medium', 'Large']

}
