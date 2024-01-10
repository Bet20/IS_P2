import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { ReleasesModule } from './releases/releases.module';
import {LabelsModule} from "./labels/labels.module";
import {ArtistsModule} from "./artists/artists.module";

@Module({
  imports: [ReleasesModule, LabelsModule, ArtistsModule],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}
