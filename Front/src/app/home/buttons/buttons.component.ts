import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-buttons',
  standalone: true,
  imports: [],
  templateUrl: './buttons.component.html',
  styleUrl: './buttons.component.css'
})


export class ButtonsComponent {
  @Input() buttonText: string = 'Button';
  @Input() styling: string = ''
  public description = 'hello'
}
