import { Module } from '@nestjs/common';
import { ReleasesService } from './releases.service';
import { ReleasesController } from './releases.controller';

@Module({
  providers: [ReleasesService],
  controllers: [ReleasesController]
})
export class ReleasesModule {}
