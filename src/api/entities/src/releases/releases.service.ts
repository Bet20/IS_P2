import {Injectable} from '@nestjs/common';
import {PrismaClient} from '@prisma/client';

@Injectable()
export class ReleasesService {
    private prisma = new PrismaClient();

    async findAll({skip = 0, take = 10}: { skip?: number; take?: number } = {}): Promise<any[]> {
        return this.prisma.releases.findMany({
            skip,
            take,
        });
    }

    async getPageCount({size = 10}): Promise<any> {
        return Math.ceil((await this.prisma.releases.count()) / size);
    }

    async create(d: any): Promise<any> {
        return this.prisma.releases.create({
            data: {
                id: d.id,
                title: d.title,
                genre: d.genre,
                style: d.style,
                year: d.year,
                artist_id: d.artist_id,
                label_id: d.label_id,
                country: d.country,
            }
        });
    }
}
