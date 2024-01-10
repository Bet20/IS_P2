import {Body, Controller, Get, Post, Query} from '@nestjs/common';
import {ReleasesService} from './releases.service';

@Controller('releases')
export class ReleasesController {
    constructor(private readonly releasesService: ReleasesService) {
    }

    @Get()
    async findAll(@Query('page') page: number = 1) {
        const pageSize = 10;
        const skip = (page - 1) * pageSize;

        return this.releasesService.findAll({skip, take: pageSize});
    }

    @Get("pageCount")
    async pageCount(@Query('size') size: number = 10) {
        return this.releasesService.getPageCount({size})
    }

    @Post()
    async create(@Body() body: {
        id: number,
        title: string,
        genre: string,
        style: string,
        year: string,
        artist_id: number,
        label_id: number,
        country: number
    }) {
        const {id, title, genre, style, year, artist_id, label_id, country} = body;
        return this.releasesService.create({id, title, genre, style, year, artist_id, label_id, country});
    }
}
